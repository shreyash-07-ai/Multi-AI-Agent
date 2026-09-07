import time
import random

from google import genai
from google.genai import types

from app.config import GEMINI_API_KEYS, GEMINI_MODEL


# Store Gemini clients
_clients = []


def clients():
    """
    Create one Gemini client for each configured API key.
    """

    global _clients

    if not GEMINI_API_KEYS:
        raise RuntimeError(
            "No Gemini API keys found. "
            "Add GEMINI_API_KEY_1, GEMINI_API_KEY_2, etc. to .env"
        )

    if not _clients:
        _clients = [
            genai.Client(api_key=api_key)
            for api_key in GEMINI_API_KEYS
        ]

    return _clients


def _is_retryable_error(error):
    """
    Check whether the Gemini error is temporary.
    """

    error_text = str(error).upper()

    retry_errors = [
        "429",
        "RESOURCE_EXHAUSTED",
        "RATE_LIMIT",
        "TOO MANY REQUESTS",
        "503",
        "UNAVAILABLE",
        "500",
        "502",
        "504",
        "INTERNAL",
        "TIMEOUT",
        "TIMED OUT",
        "DEADLINE_EXCEEDED",
        "SERVICE UNAVAILABLE",
    ]

    return any(
        item in error_text
        for item in retry_errors
    )


def ask(system: str, user: str) -> str:
    """
    Generate Gemini response using multiple API keys.

    If one API key fails, the next API key is used.
    """

    gemini_clients = clients()

    last_error = None

    # Try every Gemini API key
    for key_index, gemini_client in enumerate(gemini_clients):

        key_number = key_index + 1

        print(
            f"\nUsing Gemini API key #{key_number} "
            f"| model={GEMINI_MODEL}"
        )

        # Retry current key twice
        for attempt in range(2):

            try:

                response = gemini_client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=user,
                    config=types.GenerateContentConfig(
                        system_instruction=system,
                        temperature=0.3,
                    ),
                )

                text = getattr(
                    response,
                    "text",
                    None
                )

                if not text:
                    raise RuntimeError(
                        f"Gemini returned an empty response "
                        f"using API key #{key_number}"
                    )

                print(
                    f"Gemini API key #{key_number} "
                    f"worked successfully."
                )

                return text

            except Exception as error:

                last_error = error

                print(
                    f"Gemini error | "
                    f"key=#{key_number} | "
                    f"attempt={attempt + 1}/2 | "
                    f"error={error}"
                )

                # If error is permanent,
                # immediately move to next key.
                if not _is_retryable_error(error):
                    break

                # Retry the same key once
                if attempt < 1:

                    delay = (
                        2 ** (attempt + 1)
                        + random.uniform(0, 1)
                    )

                    print(
                        f"Retrying Gemini API key "
                        f"#{key_number} "
                        f"in {delay:.1f} seconds..."
                    )

                    time.sleep(delay)

        # Current key failed
        print(
            f"Gemini API key #{key_number} failed. "
            f"Switching to next API key..."
        )

    # All keys failed
    raise RuntimeError(
        "All Gemini API keys failed. "
        f"Last error: {last_error}"
    )