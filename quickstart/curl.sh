#!/usr/bin/env bash
# HeFu quickstart with plain curl — no SDK required.
#
# Setup:
#   export HEFU_API_KEY="sk-hefu-..."
#   bash quickstart/curl.sh

set -euo pipefail

if [ -z "${HEFU_API_KEY:-}" ]; then
  echo "HEFU_API_KEY is not set. Export it first, e.g.: export HEFU_API_KEY=sk-hefu-..." >&2
  exit 1
fi

BASE_URL="https://api.hefu.hk/v1"

# 1. List available models (OpenAI-compatible GET /v1/models).
echo "=== Models ==="
curl -sS "${BASE_URL}/models" \
  -H "Authorization: Bearer ${HEFU_API_KEY}"
echo

# 2. Chat completion (OpenAI-compatible POST /v1/chat/completions).
#    Swap "model" for any ID from https://www.hefu.hk/models
echo "=== Chat completion (deepseek-v4-pro) ==="
curl -sS "${BASE_URL}/chat/completions" \
  -H "Authorization: Bearer ${HEFU_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4-pro",
    "messages": [
      {"role": "system", "content": "You are a concise assistant."},
      {"role": "user", "content": "In one sentence, what is an API gateway?"}
    ],
    "temperature": 0.3,
    "max_tokens": 120
  }'
echo
