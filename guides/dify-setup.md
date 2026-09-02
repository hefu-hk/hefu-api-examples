# Set Up HeFu in Dify

Dify's **OpenAI-API-compatible** model provider lets you register any endpoint that speaks the OpenAI chat-completions schema — which is exactly what HeFu exposes. Each model is added once and then becomes available to every app in the workspace.

> UI labels below reflect recent Dify versions; menu placement moves between releases, so **treat exact paths as approximate — follow the current version's UI**.

## Prerequisites

- A Dify workspace (cloud or self-hosted) with permission to manage model providers.
- A HeFu API key — [sign up](https://hefu.hk/login?mode=register&ref=Q8E2RWHR) and create one in the [console](https://www.hefu.hk).

## Steps

1. Open your workspace settings: click your **profile avatar → Settings → Model Provider** (in some versions: **Settings → Model Provider** from the left sidebar).
2. Find **OpenAI-API-compatible** in the provider list and click **Add model** (or install the provider plugin first if prompted — plugin-based providers are the default in recent versions).
3. Fill in the model form:
   - **Model Name:** an exact ID from the [HeFu catalog](https://www.hefu.hk/models), e.g. `deepseek-v4-pro`
   - **API Key:** your HeFu key
   - **API endpoint URL:** `https://api.hefu.hk/v1` (no trailing `/chat/completions` — Dify appends the path itself)
   - **Completion mode:** `Chat`
   - **Model context size / Upper bound for max tokens:** set to match the model (check the catalog/docs; conservative defaults like 32k context and 4k max tokens are safe starting points)
   - **Function calling:** enable only for models with native tool support (e.g. `deepseek-v4-pro`, `gpt-5.5`, `claude-opus-5`); set to `Not support` otherwise
   - **Vision support:** enable only for multimodal models (e.g. `qwen3.7-max`, `glm-5.1`)
4. Save. Repeat **Add model** for each HeFu model you want — suggested starter set:
   - General chat: `deepseek-v4-pro`, `kimi-k2.6`, `gpt-5.5`
   - Agent / tool use: `claude-opus-5`, `kimi-k3`
   - Budget: `deepseek-v4-flash`, `qwen3.6-plus`, `minimax-m2.5`
5. Open an app (or create one), open the **model selector** in the orchestrate/prompt panel, and pick one of the HeFu models. Send a test message in the debug panel.

## Troubleshooting

- **Credential validation fails** — check the endpoint URL ends with `/v1` and the key has no stray whitespace.
- **Model not found** — the Model Name must match the catalog ID verbatim, including dots (`kimi-k2.6`, not `kimi-k26`).
- **Tool calls silently dropped** — the model was saved with function calling enabled but doesn't support it natively; edit the model entry and disable the toggle.

## Notes

- The OpenAI-API-compatible provider stores credentials per model entry; rotating a key means editing each saved model (or re-adding them). Keep the key in your secrets manager, e.g. as `HEFU_API_KEY`.
- For workflows that fan out across models, see [Fallback routing](fallback-routing.md) for an application-side pattern you can mirror in a Dify workflow's branching.

See also: [n8n setup](n8n-setup.md) · [Cline setup](cline-setup.md) · [Fallback routing](fallback-routing.md)
