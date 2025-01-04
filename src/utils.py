import os
import random
import pytimeparse
from dotenv import load_dotenv


load_dotenv()


class DotDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )


def read_env():
    interval = os.environ.get("INTERVAL")
    interval = 1800 if interval is None else pytimeparse.parse(interval)

    interval_var = os.environ.get("INTERVAL_VAR")
    interval_var = 0 if interval_var is None else pytimeparse.parse(interval_var)

    system_prompt = os.environ.get("SYSTEM_PROMPT")
    if system_prompt is None:
        raise Exception(f"Not found: {system_prompt=}")

    user_prompt = os.environ.get("USER_PROMPT")
    if user_prompt is None:
        user_prompt = ["generate"]
    else:
        user_prompt = user_prompt.split("|~|")
        user_prompt = [" ".join(u.split()) for u in user_prompt]

    model_name = os.environ.get("GROQ_MODEL")
    model_name = "llama-3.1-8b-instant" if model_name is None else model_name

    return DotDict(
        TWITTER_API_KEY=os.environ.get("TWITTER_API_KEY"),
        TWITTER_API_SECRET=os.environ.get("TWITTER_API_SECRET"),
        TWITTER_ACCESS_TOKEN=os.environ.get("TWITTER_ACCESS_TOKEN"),
        TWITTER_ACCESS_TOKEN_SECRET=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
        interval=interval,
        interval_var=interval_var,
        model_name=model_name,
        system_prompt=system_prompt,
        user_prompts=user_prompt,
    )


def calc_pause(interval: int, interval_var: int):
    if interval_var is None:
        return interval
    if interval_var > interval:
        raise Exception(f"{interval_var=} > {interval=}")

    extra_pause = random.choice([interval_var, -1 * interval_var])
    return interval - extra_pause


def convert_uprompt(x: list):
    x = [" ".join(u.split()) for u in x]
    return "|~|".join(x)


def ensure_tweet_len(x, max_len=280):
    actual_text = x.encode("utf-8")
    actual_len = len(actual_text)
    if actual_len <= max_len:
        return x

    return actual_text[:max_len].decode("utf-8")
