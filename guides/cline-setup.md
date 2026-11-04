# Set Up HeFu in Cline (VS Code)

Point Cline at HeFu's OpenAI-compatible endpoint to run any model in the [HeFu catalog](https://www.hefu.hk/models) from VS Code's agentic coding assistant. Setup takes about five minutes.

> In-depth companion article with troubleshooting tables and background:
> [Cline VS Code Custom OpenAI-Compatible Provider Setup](https://blog.hefu.hk/en/blog/cline-vs-code-custom-openai-compatible-provider-setup)

## Prerequisites

- VS Code with the **Cline** extension installed from the marketplace.
- A HeFu API key — [sign up](https://hefu.hk/login?mode=register&ref=Q8E2RWHR) and create one in the [console](https://www.hefu.hk).

## Steps

1. Open VS Code and click the **Cline icon** in the activity bar.
2. Click the **gear icon** at the top of the Cline panel to open settings.
3. In the **API Provider** dropdown, select **OpenAI Compatible** (not the built-in "OpenAI" entry — that one is locked to `api.openai.com`).
4. Fill in the fields:
   - **Base URL:** `https://api.hefu.hk/v1` (must include `/v1`, no trailing slash)
   - **API Key:** your HeFu key. For shared or version-controlled workspaces, use `$HEFU_API_KEY` environment-variable syntax so the key never lands in a committed file.
   - **Model ID:** an exact ID from the [model catalog](https://www.hefu.hk/models). Note the Model ID field may sit inside a collapsible **Model Configuration** block — do not skip it. Good starting points:
     - Coding / agentic loops: `deepseek-v4-pro`, `claude-opus-5`, `gpt-5.5`
     - Budget loops: `deepseek-v4-flash`, `kimi-k3`
5. Click **Verify** (if shown in your version), then send a test prompt like `Reply with OK`.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `401 Unauthorized` | Wrong or expired key | Regenerate the key in the HeFu console; check for stray whitespace |
| `404 Not Found` | Base URL missing `/v1`, or trailing slash | Use exactly `https://api.hefu.hk/v1` |
| `Model not found` | Model ID typo or deprecated name | Copy the ID verbatim from the [catalog](https://www.hefu.hk/models) |

You can isolate endpoint problems from Cline problems with a direct call:

```bash
curl https://api.hefu.hk/v1/chat/completions \
  -H "Authorization: Bearer $HEFU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-pro","messages":[{"role":"user","content":"OK"}]}'
```

## Notes

- Cline stores the key locally; only the extension uses it. Rotate keys periodically from the HeFu console.
- Agent loops burn tokens fast — set a budget cap on the HeFu side and monitor usage in the console. Current rates are on the [pricing page](https://www.hefu.hk/pricing).
- As of this writing, Cline offers a single OpenAI-compatible slot; keep the full catalog behind HeFu and just change the Model ID to switch models.

See also: [LobeChat setup](lobechat-setup.md) · [Open WebUI setup](open-webui-setup.md) · [Fallback routing](fallback-routing.md)
