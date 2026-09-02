# Set Up HeFu in n8n

Two ways to call HeFu from n8n: the **OpenAI node / OpenAI Chat Model** (for AI agent workflows) with a custom base URL, or the generic **HTTP Request** node for full control. Both work because HeFu speaks the OpenAI API schema.

> UI labels below reflect recent n8n versions; node and credential layouts change between releases, so **treat exact paths as approximate — follow the current version's UI**.

## Prerequisites

- An n8n instance (cloud or self-hosted).
- A HeFu API key — [sign up](https://hefu.hk/login?mode=register&ref=Q8E2RWHR) and create one in the [console](https://www.hefu.hk). On self-hosted n8n, also set it as an environment variable (`HEFU_API_KEY`) if you plan to reference it via expressions.

## Option A: OpenAI credential with a custom base URL

Best for AI Agent / chain workflows that expect an OpenAI Chat Model.

1. Go to **Credentials → Add credential** and search for **OpenAI**.
2. Fill in:
   - **API Key:** your HeFu key
   - **Base URL:** `https://api.hefu.hk/v1` — this field overrides the default `https://api.openai.com/v1`. If the field is hidden in your version, look for it under the credential's advanced/advanced-options section.
3. Save the credential.
4. In your workflow, add an **AI Agent** node (or any node with a *Chat Model* input) and attach an **OpenAI Chat Model** sub-node using the credential above.
5. In the model dropdown/field, enter an exact ID from the [HeFu catalog](https://www.hefu.hk/models), e.g. `deepseek-v4-pro`, `kimi-k2.6`, or `gpt-5.5`. If the dropdown doesn't fetch HeFu's list, type the ID manually (the expression/manual entry option).
6. Run the node with a test prompt.

## Option B: HTTP Request node

Best when you need raw control over the payload (streaming flags, extra headers, non-chat endpoints).

1. Add an **HTTP Request** node.
2. Configure:
   - **Method:** `POST`
   - **URL:** `https://api.hefu.hk/v1/chat/completions`
   - **Authentication:** `Generic Credential Type` → `Header Auth`, with header name `Authorization` and value `Bearer sk-hefu-...` (or reference the env var: `={{ 'Bearer ' + $env.HEFU_API_KEY }}`)
   - **Body Content Type:** `JSON`, body:
     ```json
     {
       "model": "deepseek-v4-flash",
       "messages": [
         {"role": "user", "content": "={{ $json.prompt }}"}
       ]
     }
     ```
3. Execute the node and inspect the response under `choices[0].message.content`.

## Troubleshooting

- **401 Unauthorized** — wrong key or missing `Bearer ` prefix (HTTP node) / wrong credential (OpenAI node).
- **404 Not Found** — base URL must be exactly `https://api.hefu.hk/v1` (credential) or `https://api.hefu.hk/v1/chat/completions` (HTTP node).
- **Model not found** — copy the ID verbatim from the [catalog](https://www.hefu.hk/models).

## Notes

- n8n's built-in **Error Trigger / retry-on-fail** settings handle transient failures; for model-level fallback (e.g. `deepseek-v4-flash` → `qwen3.6-plus` → `kimi-k2.6`), chain nodes with an `IF` on the previous node's error output, or use the application-side pattern in [Fallback routing](fallback-routing.md).
- Keep keys in n8n credentials or environment variables, never inline in shared workflow JSON exports.

See also: [Dify setup](dify-setup.md) · [Fallback routing](fallback-routing.md)
