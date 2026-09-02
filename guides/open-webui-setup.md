# Set Up HeFu in Open WebUI

Point Open WebUI at HeFu's OpenAI-compatible endpoint. Two fields in the admin UI — or two environment variables — and the full [HeFu catalog](https://www.hefu.hk/models) appears in the model dropdown alongside your local models.

> In-depth companion article with multi-endpoint configuration and edge cases:
> [Open WebUI Custom OpenAI API Endpoint Setup](https://blog.hefu.hk/en/blog/open-webui-custom-openai-api-endpoint-setup)

## Prerequisites

- A running Open WebUI instance (Docker is most common; the official quick start maps host port 3000 to container port 8080).
- A HeFu API key — [sign up](https://hefu.hk/login?mode=register&ref=Q8E2RWHR) and create one in the [console](https://www.hefu.hk).

## Method 1: Admin panel UI

1. Open **Admin Settings → Connections**.
2. In the OpenAI API section, set:
   - **API Base URL:** `https://api.hefu.hk/v1`
   - **API Key:** your HeFu key
3. Click **Save**, then refresh the page.

Open WebUI calls `GET /v1/models` on the endpoint automatically, so the HeFu models appear in the selector within seconds — no manual ID entry needed. Verify with a new chat and a short test message.

## Method 2: Environment variables (Docker / headless)

```bash
OPENAI_API_BASE_URLS=https://api.hefu.hk/v1
OPENAI_API_KEYS=sk-hefu-...
```

Both variables accept comma-separated lists if you want HeFu alongside other backends. Docker Compose example:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OPENAI_API_BASE_URLS=https://api.hefu.hk/v1
      - OPENAI_API_KEYS=${HEFU_API_KEY}
    volumes:
      - open-webui:/app/backend/data
```

## Troubleshooting

- **401 Unauthorized** — wrong/expired key; regenerate in the HeFu console and re-enter it under Connections.
- **404 Not Found** — base URL missing the `/v1` suffix; append it and re-save.
- **Models don't load** — the endpoint isn't answering `GET /v1/models`. Test directly:
  ```bash
  curl https://api.hefu.hk/v1/models -H "Authorization: Bearer $HEFU_API_KEY"
  ```
- **TLS errors** — a corporate proxy or self-signed cert is interfering; check the container's CA store.

## Notes

- Local Ollama models keep working alongside the HeFu endpoint in the same model selector.
- To revert, clear the two fields in Connections (or remove the env vars and restart).
- Prefer environment variables over the UI database for keys, and restrict Admin Settings access — anyone with admin rights can read endpoint keys.

See also: [Cline setup](cline-setup.md) · [LobeChat setup](lobechat-setup.md) · [Fallback routing](fallback-routing.md)
