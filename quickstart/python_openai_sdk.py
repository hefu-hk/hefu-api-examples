"""HeFu quickstart with the official OpenAI Python SDK.

HeFu exposes an OpenAI-compatible API, so the only change versus a stock
OpenAI setup is `base_url` — every other call stays identical.

Setup:
    pip install openai
    export HEFU_API_KEY="sk-hefu-..."
    python quickstart/python_openai_sdk.py
"""

import os

from openai import OpenAI

# Read the key from the environment; never hard-code keys in source.
api_key = os.environ.get("HEFU_API_KEY")
if not api_key:
    raise SystemExit("HEFU_API_KEY is not set. Export it first, e.g.: export HEFU_API_KEY=sk-hefu-...")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.hefu.hk/v1",  # the only line that differs from a stock OpenAI client
)

# A spread of flagship models available through the same endpoint and key.
# See https://www.hefu.hk/models for the full catalog.
MODELS = [
    "deepseek-v4-pro",
    "kimi-k2.6",
    "claude-opus-5",
]

for model in MODELS:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": "In one sentence, what is an API gateway?"},
        ],
        temperature=0.3,
        max_tokens=120,
    )
    print(f"--- {model} ---")
    print(response.choices[0].message.content)
    print(f"(tokens: {response.usage.total_tokens})\n")
