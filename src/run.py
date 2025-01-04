import time
import tweepy
import random
import logging
from groq import Groq
from loguru import logger
from tenacity import retry, wait_fixed, before_log
from utils import read_env, calc_pause, ensure_tweet_len


config = read_env()

groq_client = Groq(api_key=config.GROQ_API_KEY)
twitter_client = tweepy.Client(
    consumer_key=config.TWITTER_API_KEY,
    consumer_secret=config.TWITTER_API_SECRET,
    access_token=config.TWITTER_ACCESS_TOKEN,
    access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
)


def log_retry_error(retry_state):
    logger.error(
        f"Attempt {retry_state.attempt_number} failed with exception: {retry_state.outcome.exception()}"
    )


@retry(
    wait=wait_fixed(30), before=before_log(logger, logging.DEBUG), after=log_retry_error
)
def send_once():
    user_prompt = random.choice(config.user_prompts)
    logger.info(f"{user_prompt=}")

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": config.system_prompt,
            },
            {"role": "user", "content": user_prompt},
        ],
        model=config.model_name,
    )
    response = chat_completion.choices[0].message.content
    response = " ".join(response.split())
    logger.info(f"{response=}")

    # ensure can tweet
    logger.debug("Ensuring tweet length")
    tweet_text = ensure_tweet_len(x=response, max_len=280)
    # tweet
    logger.debug(f"Tweeting: {tweet_text}")
    twitter_client.create_tweet(text=tweet_text)

    pause = calc_pause(interval=config.interval, interval_var=config.interval_var)
    logger.info(f"Will sleep for {pause} secs")
    time.sleep(pause)


while True:
    send_once()
