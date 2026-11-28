#!/usr/bin/env bash
# HeFu quickstart with plain curl — no SDK required.
#
# Setup:
#   export HEFU_API_KEY="sk-hefu-..."
#   export HEFU_MODEL="deepseek-v4-flash"  # optional current model override
#   bash quickstart/curl.sh

set -euo pipefail

if [ -z "${HEFU_API_KEY:-}" ]; then
  echo "HEFU_API_KEY is not set. Export it first, e.g.: export HEFU_API_KEY=sk-hefu-..." >&2
  exit 1
fi

BASE_URL="https://api.hefu.hk/v1"
MODEL="${HEFU_MODEL:-deepseek-v4-flash}"
if [[ ! "$MODEL" =~ ^[A-Za-z0-9._:-]+$ ]]; then
  echo "HEFU_MODEL contains unsupported characters. Copy the exact ID from https://hefu.hk/models" >&2
  exit 1
fi

# 1. List available models (OpenAI-compatible GET /v1/models).
echo "=== Models ==="
curl -sS "${BASE_URL}/models" \
  -H "Authorization: Bearer ${HEFU_API_KEY}"
echo

# 2. Chat completion (OpenAI-compatible POST /v1/chat/completions).
#    Swap the model through HEFU_MODEL when the live catalog changes.
echo "=== Chat completion (${MODEL}) ==="
payload=$(printf '{"model":"%s","messages":[{"role":"system","content":"You are a concise assistant."},{"role":"user","content":"In one sentence, what is an API gateway?"}],"temperature":0.3,"max_tokens":120}' "$MODEL")
curl -sS "${BASE_URL}/chat/completions" \
  -H "Authorization: Bearer ${HEFU_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$payload"
echo
