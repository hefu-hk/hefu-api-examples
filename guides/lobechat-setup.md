# Set Up HeFu in LobeChat

Add HeFu as a custom OpenAI-compatible provider in LobeChat and route the whole [HeFu catalog](https://www.hefu.hk/models) through LobeChat's native interface with one API key.

> In-depth companion article with capability-toggle details and comparisons:
> [How to Set Up HeFu as a Custom Provider in LobeChat](https://blog.hefu.hk/en/blog/lobechat-custom-provider-hefu-setup-guide)

## Prerequisites

- A running LobeChat instance — cloud or self-hosted (Docker, Vercel, desktop). The custom-provider settings are the same in both.
- A HeFu API key — [sign up](https://hefu.hk/login?mode=register&ref=Q8E2RWHR) and create one in the [console](https://www.hefu.hk).

## Steps

1. Open **Settings → Language Model**.
2. Click **Add Custom Provider**.
3. Fill in the fields:
   - **Display name:** `HeFu`
   - **Base URL:** `https://api.hefu.hk/v1`
   - **API key:** your HeFu key
   - **HTTP proxy (optional):** only if your network needs a proxy to reach `api.hefu.hk`.
4. Save the provider.
5. In the provider's model list, add each model ID exactly as documented in the [HeFu catalog](https://www.hefu.hk/models), for example:
   - General / agentic: `gpt-5.5`, `claude-opus-5`, `kimi-k3`
   - Long-context Chinese text: `kimi-k3`, `deepseek-v4-pro`
   - Multimodal: `qwen3.7-max`, `glm-5.1`
   - Budget: `deepseek-v4-flash`, `MiniMax-M2.5`
6. Enable capability toggles per provider: **function calling** for tool-using models, **vision** only for multimodal models. Enabling vision on a non-vision model can cause silent failures — toggle conservatively.
7. Start a new conversation, pick a HeFu model, and send a test message.

## Troubleshooting

- **401 Unauthorized** — wrong/expired key or copied whitespace; regenerate in the HeFu console.
- **404 Not Found** — base URL must end with `/v1`, not `/chat/completions`.
- **Model not found** — the ID doesn't match the catalog; re-check for typos.
- Self-hosted Docker with a legacy `OPENAI_PROXY_URL` set: it can override UI-configured endpoints in some versions — unset it and restart the container.

## Notes

- When HeFu adds models, edit the provider's model list and add the new IDs; the saved API key persists.
- For self-hosted deployments, pass the key as an environment variable (`-e HEFU_API_KEY=...` or your tooling's equivalent) rather than storing it in shared config files.

See also: [Cline setup](cline-setup.md) · [Open WebUI setup](open-webui-setup.md) · [Fallback routing](fallback-routing.md)
