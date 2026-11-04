# HeFu API Examples

<!-- Badges: update the repo URLs after publishing -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Models](https://img.shields.io/badge/models-catalog-blue)](https://www.hefu.hk/models)
[![Docs](https://img.shields.io/badge/docs-hefu.hk-green)](https://www.hefu.hk/docs)
<!-- TODO: add CI / release badges once the repository is public -->

**HeFu is an enterprise AI application platform: a full-modality model workbench, scenario-based office tools and third-party app integration, all behind one OpenAI-compatible API.** One base URL and one API key give you access to frontier models from OpenAI, Anthropic, Google, DeepSeek, Moonshot (Kimi), Alibaba (Qwen), Zhipu (GLM), MiniMax and more — text, image, video and voice.

- **Base URL:** `https://api.hefu.hk/v1`
- **Auth:** `Authorization: Bearer <your API key>` (user key) or an OAuth 2.0 user token (app integration)
- **API surface:** OpenAI-compatible (`/v1/chat/completions`, `/v1/models`, …) plus images, video jobs, speech and embeddings — see the [OpenAPI contract](https://hefu.hk/openapi.yaml)
- **No code?** The [model workbench](https://www.hefu.hk/models) covers full-modality online debugging, scenario presets and a private results center in the browser.

## Repository layout

Two layers, one repo:

- **[quickstart/](quickstart/) — calling the API** with your own key: chat, multimodal (image / audio / video), and raw HTTP.
- **[app-integration/](app-integration/) — building on top of HeFu**: OAuth + PKCE integration where your users pay for their own usage and your app holds no keys.
- **[guides/](guides/) — connecting tools** (Cline, LobeChat, Open WebUI, Dify, n8n) and the model workbench walkthrough.
- **[examples/](examples/) — production patterns** such as the fallback chain.

## Quick start

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

# Multimodal: image + speech + async video (pip install openai requests)
python quickstart/multimodal.py
```

### Models used in these examples

`kimi-k3`, `claude-opus-4.5`, `gpt-6.1-terra` (chat quickstarts); image/audio/video IDs are resolved at runtime from `GET /v1/models` because the catalog changes constantly — check the [model catalog](https://www.hefu.hk/models) for the live list (as of 2026-11).

## Repository index

| Path | Description |
|---|---|
| [quickstart/python_openai_sdk.py](quickstart/python_openai_sdk.py) | Official Python `openai` SDK with a custom `base_url`; calls three models |
| [quickstart/node_openai_sdk.mjs](quickstart/node_openai_sdk.mjs) | Official Node `openai` SDK with a custom `baseURL`; calls three models |
| [quickstart/curl.sh](quickstart/curl.sh) | Raw HTTP calls: model list + chat completion |
| [quickstart/multimodal.py](quickstart/multimodal.py) | Image generation, text-to-speech and async video generation through one key |
| [app-integration/oauth_pkce.py](app-integration/oauth_pkce.py) | Zero-cost third-party integration: OAuth + PKCE without a client secret |
| [guides/cline-setup.md](guides/cline-setup.md) | Use HeFu as Cline's OpenAI-compatible provider in VS Code |
| [guides/lobechat-setup.md](guides/lobechat-setup.md) | Add HeFu as a custom provider in LobeChat |
| [guides/open-webui-setup.md](guides/open-webui-setup.md) | Point Open WebUI at the HeFu endpoint (UI or env vars) |
| [guides/dify-setup.md](guides/dify-setup.md) | Configure HeFu as an OpenAI-API-compatible model provider in Dify |
| [guides/n8n-setup.md](guides/n8n-setup.md) | Use HeFu from n8n's OpenAI node and HTTP Request node |
| [guides/workbench.md](guides/workbench.md) | Model workbench walkthrough: debugging, presets, results center, sub-accounts |
| [guides/fallback-routing.md](guides/fallback-routing.md) | Application-layer fallback chain design (429/5xx handling) |
| [examples/fallback.py](examples/fallback.py) | Runnable fallback chain across several models |

## Client guidance

- Set client timeouts **≥120 seconds** (streaming is unaffected — time-to-first-byte is fast).
- On 429/5xx, retry with exponential backoff; the gateway fails over across upstream channels automatically.

## Resources

- [HeFu console](https://www.hefu.hk) — sign up, API keys, usage
- [Developer platform](https://www.hefu.hk/docs) — quickstart, live debugging, OAuth integration
- [Model catalog](https://www.hefu.hk/models)
- [API documentation](https://www.hefu.hk/docs)
- [Pricing](https://www.hefu.hk/pricing)
- [Status](https://www.hefu.hk/status)
- [HeFu engineering blog (EN)](https://blog.hefu.hk/en/blog/) — in-depth tutorials and comparisons

## License

[MIT](LICENSE)
