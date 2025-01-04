# Groq Twitter

Automatically generate and schedule tweets using [Groq](https://groq.com/). Set tweets to be posted at predetermined intervals, ensuring consistent engagement without manual effort.

## Usage

Via `docker`:

```bash
docker run \
    --restart=always \
    -d \
    --name groq-twitter \
    -e GROQ_MODEL='llama-3.1-8b-instant' \
    -e GROQ_API_KEY='' \
    -e TWITTER_API_KEY='' \
    -e TWITTER_API_SECRET='' \
    -e TWITTER_ACCESS_TOKEN='' \
    -e TWITTER_ACCESS_TOKEN_SECRET='' \
    -e SYSTEM_PROMPT='Hello, im your virtual assistant here to help with any questions about our services. What would you like to know more about today?' \
    -e USER_PROMPT='Can you explain how your pricing model works?|~|What are the working hours for customer support?' \
    -e INTERVAL='30m' \
    -e INTERVAL_VAR='5m' \
    ghcr.io/minky2858/groq-twitter:latest
```

Or with `docker-compose`, refer to [example](/examples/docker-compose.yml)

## Env Vars

-   `GROQ_MODEL`: Specifies the Groq model to use for processing. Default is set to llama-3.1-8b-instant. For more models, refer to the Groq Model [Documentation](https://console.groq.com/docs/models).
-   `GROQ_API_KEY`: Your API key for accessing Groq services.
-   `TWITTER_API_KEY`: API key used to authenticate with the Twitter API.
-   `TWITTER_API_SECRET`: API secret for the Twitter API.
-   `TWITTER_ACCESS_TOKEN`: Access token for interacting with Twitter on behalf of your Twitter account.
-   `TWITTER_ACCESS_TOKEN_SECRET`: Access token secret for securing interactions with Twitter.
-   `SYSTEM_PROMPT`: A predefined system prompt that the application uses to initiate interactions or processes.
-   `USER_PROMPT`: Optional user-defined prompts to customize interactions. This variable can include multiple prompts separated by `|~|`. For example, prompt1|~|prompt2.
-   `INTERVAL`: The base interval in seconds between actions or checks performed by the application. Must be specified as an integer.
-   `INTERVAL_VAR`: Specifies the variation in seconds that can be added to or subtracted from `INTERVAL` to introduce randomness to the timing of actions. Defaults to `0` if not set.
