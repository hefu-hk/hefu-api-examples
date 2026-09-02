# HeFu API Examples

<!-- Badges: update the repo URLs after publishing -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Models](https://img.shields.io/badge/models-catalog-blue)](https://www.hefu.hk/models)
[![Docs](https://img.shields.io/badge/docs-hefu.hk-green)](https://www.hefu.hk/docs)
<!-- TODO: add CI / release badges once the repository is public -->

Ready-to-run examples and setup guides for [HeFu](https://www.hefu.hk), an OpenAI-compatible AI API aggregation gateway. One base URL and one API key give you access to frontier models from OpenAI, Anthropic, DeepSeek, Moonshot (Kimi), Alibaba (Qwen), Zhipu (GLM), and MiniMax.

- **Base URL:** `https://api.hefu.hk/v1`
- **Auth:** `Authorization: Bearer <your API key>`
- **API surface:** OpenAI-compatible (`/v1/chat/completions`, `/v1/models`, etc.)

## Features

- **One key, many models** — call GPT, Claude, DeepSeek, Kimi, Qwen, GLM, and MiniMax models through a single OpenAI-compatible endpoint. No per-provider SDKs or keys.
- **Drop-in compatible** — point the official `openai` SDK (Python or Node) at the HeFu base URL and everything else stays the same.
- **Client-ready guides** — step-by-step setup for Cline, LobeChat, Open WebUI, Dify, and n8n.
- **Production patterns** — an application-layer fallback chain example that survives 429s and 5xx errors.

## Quick Start

### 1. Get an API key

[Sign up for HeFu](https://hefu.hk/login?mode=register&ref=Q8E2RWHR), then create an API key in the [console](https://www.hefu.hk). Browse the [model catalog](https://www.hefu.hk/models) and [pricing](https://www.hefu.hk/pricing) to pick your models.

### 2. Set the environment variable

All examples read the key from `HEFU_API_KEY`:

```bash
export HEFU_API_KEY="sk-hefu-..."
```

### 3. Run an example

```bash
# Python (pip install openai)
python quickstart/python_openai_sdk.py

# Node.js (npm install openai)
node quickstart/node_openai_sdk.mjs

# curl (no dependencies)
bash quickstart/curl.sh
```

### Models used in these examples

`deepseek-v4-pro`, `deepseek-v4-flash`, `kimi-k2.6`, `kimi-k3`, `qwen3.6-plus`, `qwen3.7-max`, `glm-5.1`, `minimax-m2.5`, `gpt-5.5`, `claude-opus-5`. Check the [model catalog](https://www.hefu.hk/models) for the current list.

## Repository Index

| Path | Description |
|---|---|
| [quickstart/python_openai_sdk.py](quickstart/python_openai_sdk.py) | Official Python `openai` SDK with a custom `base_url`; calls three models |
| [quickstart/node_openai_sdk.mjs](quickstart/node_openai_sdk.mjs) | Official Node `openai` SDK with a custom `baseURL`; calls three models |
| [quickstart/curl.sh](quickstart/curl.sh) | Raw HTTP calls: model list + chat completion |
| [guides/cline-setup.md](guides/cline-setup.md) | Use HeFu as Cline's OpenAI-compatible provider in VS Code |
| [guides/lobechat-setup.md](guides/lobechat-setup.md) | Add HeFu as a custom provider in LobeChat |
| [guides/open-webui-setup.md](guides/open-webui-setup.md) | Point Open WebUI at the HeFu endpoint (UI or env vars) |
| [guides/dify-setup.md](guides/dify-setup.md) | Configure HeFu as an OpenAI-API-compatible model provider in Dify |
| [guides/n8n-setup.md](guides/n8n-setup.md) | Use HeFu from n8n's OpenAI node and HTTP Request node |
| [guides/fallback-routing.md](guides/fallback-routing.md) | Application-layer fallback chain design (429/5xx handling) |
| [examples/fallback.py](examples/fallback.py) | Runnable fallback chain: `deepseek-v4-flash` → `qwen3.6-plus` → `kimi-k2.6` |

## Resources

- [HeFu console](https://www.hefu.hk) — sign up, API keys, usage
- [Model catalog](https://www.hefu.hk/models)
- [API documentation](https://www.hefu.hk/docs)
- [Pricing](https://www.hefu.hk/pricing)
- [HeFu engineering blog (EN)](https://blog.hefu.hk/en/blog/) — in-depth tutorials and comparisons

## License

[MIT](LICENSE)
