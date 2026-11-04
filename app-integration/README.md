# App Integration — zero-cost OAuth model

This directory contains a minimal, runnable example of the HeFu third-party
integration model documented at <https://www.hefu.hk/docs>:

- **The end user pays for their own model usage** through their HeFu account.
- **Your app holds no API key and no client secret** — it acts as an OAuth 2.0
  public client with PKCE (RFC 7636/8252).
- Billing, rate limits and quota all belong to the signed-in user, so an
  integration can ship without any AI cost line in your business model.

| File | What it shows |
|---|---|
| [oauth_pkce.py](oauth_pkce.py) | Build the authorize URL with an S256 PKCE challenge, exchange the code without a secret, and call `/v1/chat/completions` with the user's access token |

## Before you run

1. Register your app in the HeFu console and get a `client_id` (public client).
   The full registration flow is described on <https://www.hefu.hk/docs>.
2. Set the environment variables listed at the top of `oauth_pkce.py`.
3. Run the script once to get the authorize URL, approve in the browser, then
   exchange the returned code.

## Production checklist

- Store the `code_verifier` server-side between steps 1 and 3 (session or
  signed cookie) — the demo prints it to the terminal instead.
- Use `state` for CSRF protection; the demo omits it for brevity.
- Respect the gateway's client guidance: timeouts ≥120 s (streaming is
  unaffected — time-to-first-byte is fast) and exponential backoff on 429/5xx,
  the gateway fails over across upstream channels automatically.
- Refresh tokens: request offline access per the docs and refresh before the
  access token expires.
