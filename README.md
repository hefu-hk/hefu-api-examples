# HeFu API Examples

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Models](https://img.shields.io/badge/models-live_catalog-blue)](https://hefu.hk/models)
[![Docs](https://img.shields.io/badge/docs-hefu.hk-green)](https://hefu.hk/docs)

Runnable examples and setup guides for [HeFu](https://hefu.hk): a unified model API, an AI Tools Workspace, third-party app integration, and the DramaStudio short-drama workflow.

The API is OpenAI-compatible. Use one base URL and one API key for the currently listed text, image, video, voice, embedding, and search models. AI Tools and DramaStudio also provide no-code workflows for users who do not need direct API control.

- **API base URL:** `https://api.hefu.hk/v1`
- **Authentication:** `Authorization: Bearer <your API key>` for your own account, or an OAuth user token for app integration
- **Contract:** [OpenAPI specification](https://hefu.hk/openapi.yaml) and [developer documentation](https://hefu.hk/docs)
- **Live availability:** [model catalog](https://hefu.hk/models) and [current platform rates](https://hefu.hk/pricing)

## Choose your path

| Product or task | Start here |
|---|---|
| Call models with Python, Node.js or curl | [quickstart/](quickstart/) |
| Test models without writing code | [Model workbench guide](guides/workbench.md) |
| Add AI to a third-party application with OAuth + PKCE | [app-integration/](app-integration/) |
| Produce task-oriented content without code | [AI Tools Workspace guide](guides/ai-tools.md) |
| Create and review a short-drama project | [DramaStudio guide](guides/dramastudio.md) |
| Connect Cline, LobeChat, Open WebUI, Dify or n8n | [guides/](guides/) |
| Add bounded retries and model fallback | [Fallback pattern](guides/fallback-routing.md) |

## Quick start

### 1. Get access

[Sign up for HeFu](https://hefu.hk/login?mode=register&ref=Q8E2RWHR&utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-signup), create an API key in the console, and choose a currently available model from the [live catalog](https://hefu.hk/models). Check the current platform rate and billing unit on its model detail page.

### 2. Configure the key

```bash
export HEFU_API_KEY="sk-hefu-..."
```

Never commit the key. This repository's `.gitignore` excludes `.env` files, local OAuth session data, and generated output.

### 3. Run a text example

```bash
# Python: pip install openai
python quickstart/python_openai_sdk.py

# Node.js: npm install openai
node quickstart/node_openai_sdk.mjs

# Raw HTTP, no SDK dependency
bash quickstart/curl.sh
```

The chat quickstarts use `kimi-k3`, `claude-fable-5-2`, and `gpt-6.1-terra`, verified against the live catalog on 2026-11-21. Replace them when the catalog changes, or set `HEFU_MODEL` where supported.

### 4. Run a selected multimodal example

```bash
# pip install openai requests
python quickstart/multimodal.py --image
python quickstart/multimodal.py --audio
python quickstart/multimodal.py --video
```

Each option performs a real billable request; the script does not run all modalities by default. Image and audio examples try known ID prefixes, while video requires an explicit current model ID:

```bash
export HEFU_VIDEO_MODEL="<current video model ID>"
# Optional overrides: HEFU_IMAGE_MODEL, HEFU_AUDIO_MODEL, HEFU_AUDIO_VOICE
```

See the [OpenAPI specification](https://hefu.hk/openapi.yaml) for model-specific parameters and video task status fields.

## Repository index

| Path | What it demonstrates |
|---|---|
| [quickstart/python_openai_sdk.py](quickstart/python_openai_sdk.py) | Official OpenAI Python SDK with a custom `base_url` |
| [quickstart/node_openai_sdk.mjs](quickstart/node_openai_sdk.mjs) | Official OpenAI Node SDK with a custom `baseURL` |
| [quickstart/curl.sh](quickstart/curl.sh) | Model listing and chat completion over raw HTTP |
| [quickstart/multimodal.py](quickstart/multimodal.py) | Explicitly selected image, speech, and asynchronous video calls |
| [app-integration/oauth_pkce.py](app-integration/oauth_pkce.py) | OAuth authorization code flow with S256 PKCE and state validation |
| [examples/fallback.py](examples/fallback.py) | Bounded retries and fallback across current catalog models |
| [guides/workbench.md](guides/workbench.md) | Model catalog, online workbench, results, and team access |
| [guides/ai-tools.md](guides/ai-tools.md) | No-code AI Tools Workspace workflow |
| [guides/dramastudio.md](guides/dramastudio.md) | Managed short-drama production and review workflow |
| [guides/fallback-routing.md](guides/fallback-routing.md) | When to retry, fall back, or fail fast |

## Client guidance

- Use a client timeout appropriate to the workload; the current developer guidance recommends at least 120 seconds for long-running calls.
- Retry 429/5xx and network failures with bounded exponential backoff and jitter.
- Treat fallback models as different models: evaluate output quality instead of assuming interchangeable behavior.
- Reconcile actual charges against HeFu call records, wallet details, and applicable discounts.

## Get help or discuss an integration

- For a reproducible technical question, open an [integration issue](https://github.com/hefu-hk/hefu-api-examples/issues/new?template=integration-help.yml). Never post keys, tokens, wallet details, or confidential customer data.
- For solution evaluation, commercial integration, or partnership inquiries, use the [HeFu enterprise contact page](https://hefu.hk/enterprise?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-business).

## Resources

- [HeFu console](https://hefu.hk) — accounts, keys, usage, and wallet
- [Developer documentation](https://hefu.hk/docs)
- [Live model catalog](https://hefu.hk/models)
- [AI Tools Workspace](https://hefu.hk/tools)
- [DramaStudio](https://drama.hefu.hk/)
- [HeFu engineering blog](https://blog.hefu.hk/en/blog/)
- [Service status](https://hefu.hk/status)

## License

[MIT](LICENSE)
