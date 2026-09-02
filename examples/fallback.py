"""Application-layer fallback chain over HeFu's OpenAI-compatible endpoint.

Tries models in order — deepseek-v4-flash -> qwen3.6-plus -> kimi-k2.6 —
retrying transient failures (429 / 5xx / network) with backoff before
switching to the next model. Client errors (4xx other than 429) fail fast:
every model would reject an invalid request identically.

Setup:
    pip install openai
    export HEFU_API_KEY="sk-hefu-..."
    python examples/fallback.py
"""

import os
import random
import time

from openai import APIError, APIStatusError, APITimeoutError, OpenAI

# Ordered fallback chain: cheapest/fastest first, strongest last.
# Swap in any IDs from https://www.hefu.hk/models to fit your priorities.
FALLBACK_CHAIN = ["deepseek-v4-flash", "qwen3.6-plus", "kimi-k2.6"]

MAX_RETRIES_PER_MODEL = 2   # attempts per model before falling back
BACKOFF_BASE_SECONDS = 0.5  # exponential backoff: 0.5s, 1s, ... (+ jitter)
REQUEST_TIMEOUT = 30.0      # per-request timeout in seconds


def is_retryable(exc: Exception) -> bool:
    """Only fall back on infrastructure errors, never on client errors."""
    if isinstance(exc, APIStatusError):
        # 429 (rate limit) and 5xx (server side) are worth retrying/switching.
        return exc.status_code == 429 or exc.status_code >= 500
    # Timeouts and connection errors may be transient on either side.
    return isinstance(exc, (APITimeoutError, APIError)) and not isinstance(exc, APIStatusError)


def chat_with_fallback(client: OpenAI, messages: list[dict]) -> tuple[str, str, int]:
    """Walk the fallback chain. Returns (answer, model_used, attempts)."""
    attempts = 0
    last_error: Exception | None = None

    for model in FALLBACK_CHAIN:
        for retry in range(MAX_RETRIES_PER_MODEL):
            attempts += 1
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.3,
                    max_tokens=200,
                    timeout=REQUEST_TIMEOUT,
                )
                return response.choices[0].message.content, model, attempts
            except Exception as exc:  # noqa: BLE001 — classified below
                last_error = exc
                if not is_retryable(exc):
                    raise  # client error: fail fast, don't poison the chain
                if retry < MAX_RETRIES_PER_MODEL - 1:
                    # Exponential backoff with jitter before the next attempt.
                    time.sleep(BACKOFF_BASE_SECONDS * (2**retry) + random.uniform(0, 0.25))
        # Model exhausted its retries -> fall through to the next one.

    raise RuntimeError(f"All {len(FALLBACK_CHAIN)} models failed") from last_error


def main() -> None:
    api_key = os.environ.get("HEFU_API_KEY")
    if not api_key:
        raise SystemExit("HEFU_API_KEY is not set. Export it first, e.g.: export HEFU_API_KEY=sk-hefu-...")

    client = OpenAI(api_key=api_key, base_url="https://api.hefu.hk/v1")

    answer, model_used, attempts = chat_with_fallback(
        client,
        messages=[{"role": "user", "content": "In one sentence, what is an API gateway?"}],
    )
    print(f"[answer via {model_used} after {attempts} attempt(s)]")
    print(answer)


if __name__ == "__main__":
    main()
