"""HeFu quickstart with the official OpenAI Python SDK.

Setup:
    pip install openai
    export HEFU_API_KEY="sk-hefu-..."
    export HEFU_MODEL="a-current-model-id"
    python quickstart/python_openai_sdk.py

The example makes one real, billable chat request.
"""

import os

from openai import OpenAI

api_key = os.environ.get("HEFU_API_KEY")
if not api_key:
    raise SystemExit("HEFU_API_KEY is not set. Export it first, e.g.: export HEFU_API_KEY=sk-hefu-...")

# Replace the default when the live catalog changes.
model = os.environ.get("HEFU_MODEL", "deepseek-v4-flash")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.hefu.hk/v1",
)

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
print(f"(tokens: {response.usage.total_tokens})")
