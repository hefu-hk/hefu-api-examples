# HeFu API Examples

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Models](https://img.shields.io/badge/models-live_catalog-blue)](https://hefu.hk/models?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=badge-models)
[![Docs](https://img.shields.io/badge/docs-hefu.hk-green)](https://hefu.hk/docs?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=badge-docs)

**Run your first multi-model API call in about 5 minutes.** Use HeFu's OpenAI-compatible API with runnable Python, Node.js and curl examples, then follow the matching integration guide when you are ready for production.

- **API base URL:** `https://api.hefu.hk/v1`
- **Authentication:** `Authorization: Bearer <your API key>` for your own account, or an OAuth user token for app integration
- **Current model IDs:** [live model catalog](https://hefu.hk/models?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-models)
- **Contract:** [developer documentation](https://hefu.hk/docs?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-docs) and [OpenAPI specification](https://hefu.hk/openapi.yaml?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-openapi)

> **Billing notice:** the examples make real API requests and can incur charges. The Python and Node.js quickstarts make one chat request. Check the current model rate before running them, and never run multimodal or fallback loops as unattended tests.

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/hefu-hk/hefu-api-examples.git
cd hefu-api-examples
```

### 2. Get access and choose a model

[Sign up for HeFu](https://hefu.hk/login?mode=register&ref=Q8E2RWHR&utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-signup), create an API key in the console, and copy an exact model ID from the [live catalog](https://hefu.hk/models?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=quickstart-models). The catalog is authoritative when an example's default model is no longer available.

```bash
export HEFU_API_KEY="sk-hefu-..."
export HEFU_MODEL="kimi-k3"  # Replace with a current chat model ID when needed.
```

Never commit the key. This repository's `.gitignore` excludes `.env` files, local OAuth session data, and generated output.

### 3. Run one Python request

```bash
pip install openai
python quickstart/python_openai_sdk.py
```

A successful run prints the selected model, the model's answer and token usage. This is an illustrative shape, not a recorded response:

```text
--- kimi-k3 ---
An API gateway provides a single entry point for routing and managing API requests.
(tokens: 61)
```

The exact answer and token count vary. Confirm actual usage and charges in the console rather than treating this illustration as a billing result.

### 4. Or use Node.js or curl

```bash
# Node.js: one chat request; HEFU_MODEL is supported here too.
npm install openai
node quickstart/node_openai_sdk.mjs

# Raw HTTP: list models, then make one chat request.
bash quickstart/curl.sh
```

The default IDs in the examples were checked against the live catalog on 2026-11-21. Replace them when the catalog changes. Python and Node.js accept `HEFU_MODEL`; for curl, edit the `model` field in `quickstart/curl.sh`.

## Continue with a working integration

GitHub contains the runnable implementation. The linked tutorials provide the searchable, step-by-step explanation and production checklist.

| Task | Runnable example | Tutorial |
|---|---|---|
| Make an OpenAI-compatible request with Python | [Python quickstart](quickstart/python_openai_sdk.py) | [OpenAI-compatible API with Python](https://blog.hefu.hk/en/blog/openai-compatible-api-python-quickstart?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-python-tutorial) |
| Add user-authorized AI access with OAuth + PKCE | [OAuth example](app-integration/) | [OAuth + PKCE desktop integration](https://blog.hefu.hk/en/blog/oauth-pkce-desktop-app-ai-integration?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-oauth-tutorial) |
| Add bounded retries and model fallback | [Fallback example](examples/fallback.py) | [Fallback without infinite retries](https://blog.hefu.hk/en/blog/model-fallback-without-infinite-retries?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-fallback-tutorial) |
| Connect Dify | [Dify guide](guides/dify-setup.md) | [Dify setup tutorial](https://blog.hefu.hk/en/blog/dify-openai-compatible-api-setup?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-dify-tutorial) |
| Connect n8n | [n8n guide](guides/n8n-setup.md) | [n8n setup tutorial](https://blog.hefu.hk/en/blog/n8n-openai-compatible-api-setup?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-n8n-tutorial) |
| Call image, audio or video models | [Multimodal example](quickstart/multimodal.py) | [OpenAPI specification](https://hefu.hk/openapi.yaml?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-multimodal-openapi) |
| Connect Cline, LobeChat or Open WebUI | [Client guides](guides/) | [HeFu engineering blog](https://blog.hefu.hk/en/blog/?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-client-tutorials) |

### Multimodal calls

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

## Other products

These workflows are separate from the API quickstart. Use them when you need a managed product rather than direct API control.

| Product or task | Start here |
|---|---|
| Test and compare models without writing code | [Model workbench guide](guides/workbench.md) |
| Produce task-oriented content without code | [AI Tools Workspace guide](guides/ai-tools.md) |
| Create and review a short-drama project | [DramaStudio guide](guides/dramastudio.md) |

## Repository index

| Path | What it demonstrates |
|---|---|
| [quickstart/python_openai_sdk.py](quickstart/python_openai_sdk.py) | Official OpenAI Python SDK with a custom `base_url` and one billable request |
| [quickstart/node_openai_sdk.mjs](quickstart/node_openai_sdk.mjs) | Official OpenAI Node SDK with a custom `baseURL` and one billable request |
| [quickstart/curl.sh](quickstart/curl.sh) | Model listing and chat completion over raw HTTP |
| [quickstart/multimodal.py](quickstart/multimodal.py) | Explicitly selected image, speech, and asynchronous video calls |
| [app-integration/oauth_pkce.py](app-integration/oauth_pkce.py) | OAuth authorization code flow with S256 PKCE and state validation |
| [examples/fallback.py](examples/fallback.py) | Bounded retries and fallback across current catalog models |
| [guides/fallback-routing.md](guides/fallback-routing.md) | When to retry, fall back, or fail fast |

## Troubleshooting

| Error or symptom | What to check |
|---|---|
| `HEFU_API_KEY is not set` | Export the key in the same shell before running the script. |
| `401 Unauthorized` | Check the complete active key and the `Authorization: Bearer` header; never post the key in an issue. |
| `404 Not Found` | Use base URL `https://api.hefu.hk/v1`; do not append `/chat/completions` when the SDK adds it automatically. |
| Model not found or unavailable | Copy the exact current model ID from the live catalog and set `HEFU_MODEL` where supported. |
| `429` or `5xx` | Use bounded exponential backoff with jitter; do not retry forever. See the [fallback guide](guides/fallback-routing.md). |
| Unexpected usage | Stop the script and inspect console call records and wallet details. Every retry or fallback attempt can be billable. |

## Client guidance

- Use a client timeout appropriate to the workload; the current developer guidance recommends at least 120 seconds for long-running calls.
- Retry 429/5xx and network failures with bounded exponential backoff and jitter.
- Treat fallback models as different models: evaluate output quality instead of assuming interchangeable behavior.
- Reconcile actual charges against HeFu call records, wallet details, and applicable discounts.

## Get help or discuss an integration

- For a reproducible technical question, open an [integration issue](https://github.com/hefu-hk/hefu-api-examples/issues/new?template=integration-help.yml). Never post keys, tokens, wallet details, or confidential customer data.
- For solution evaluation, commercial integration, or partnership inquiries, use the [HeFu enterprise contact page](https://hefu.hk/enterprise?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-business).

## Resources

- [HeFu console](https://hefu.hk?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=readme-console) — accounts, keys, usage, and wallet
- [Developer documentation](https://hefu.hk/docs?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=resources-docs)
- [Live model catalog](https://hefu.hk/models?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=resources-models)
- [Current platform rates](https://hefu.hk/pricing?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=resources-pricing)
- [AI Tools Workspace](https://hefu.hk/tools?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=resources-ai-tools)
- [DramaStudio](https://drama.hefu.hk/?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=resources-dramastudio)
- [HeFu engineering blog](https://blog.hefu.hk/en/blog/?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=resources-blog)
- [Service status](https://hefu.hk/status?utm_source=github&utm_medium=referral&utm_campaign=hefu-api-examples&utm_content=resources-status)

## License

[MIT](LICENSE)
