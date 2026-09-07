import time
import random

from openai import OpenAI

from app.config import XAI_API_KEY, XAI_MODEL


_client = None


def client():
    global _client

    if _client is None:
        if not XAI_API_KEY:
            raise RuntimeError("XAI_API_KEY is missing in .env")

        _client = OpenAI(
            api_key=XAI_API_KEY,
            base_url="https://api.x.ai/v1",
        )

    return _client


def _is_retryable_error(error):
    """
    Retry Grok/xAI errors that are usually temporary.
    """
    error_text = str(error).upper()

    retry_errors = [
        "429",
        "RATE_LIMIT",
        "TOO MANY REQUESTS",
        "500",
        "502",
        "503",
        "504",
        "INTERNAL",
        "TIMEOUT",
        "TIMED OUT",
        "SERVICE UNAVAILABLE",
    ]

    return any(item in error_text for item in retry_errors)


def ask(system: str, user: str) -> str:
    """
    Generate a Grok response with:
    - Automatic retries
    - Exponential backoff
    - xAI/Grok API
    """

    last_error = None

    # Try the configured Grok model
    for attempt in range(3):

        try:
            response = client().chat.completions.create(
                model=XAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": system,
                    },
                    {
                        "role": "user",
                        "content": user,
                    },
                ],
                temperature=0.3,
            )

            text = response.choices[0].message.content

            if not text:
                raise RuntimeError(
                    f"Grok returned an empty response using model: {XAI_MODEL}"
                )

            return text

        except Exception as error:
            last_error = error

            print(
                f"Grok API error | model={XAI_MODEL} | "
                f"attempt={attempt + 1}/3 | error={error}"
            )

            # Don't retry permanent errors
            if not _is_retryable_error(error):
                raise

            # Exponential backoff
            if attempt < 2:
                delay = (2 ** (attempt + 1)) + random.uniform(0, 1)

                print(
                    f"Retrying Grok in {delay:.1f} seconds..."
                )

                time.sleep(delay)

    raise RuntimeError(
        "Grok API is temporarily unavailable. "
        "All retry attempts failed. "
        f"Last error: {last_error}"
    )