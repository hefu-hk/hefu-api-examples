# Third-Party App Integration with OAuth + PKCE

This directory contains a minimal HeFu OAuth 2.0 public-client example:

- The end user authorizes your app and pays for their own model usage through their HeFu account.
- Your app uses S256 PKCE and does not need an API key or client secret for this flow.
- The demo includes `state` validation, callback parsing, and code exchange; it does not skip CSRF protection.

| File | What it shows |
|---|---|
| [oauth_pkce.py](oauth_pkce.py) | Authorize URL, PKCE challenge, local session, state validation, token exchange, and a user-authorized chat request |

## Before you run

1. Register a public application in the HeFu console as described in the [developer documentation](https://hefu.hk/docs).
2. Configure the client and callback:

```bash
export HEFU_CLIENT_ID="your-public-client-id"
export HEFU_REDIRECT_URI="http://localhost:8000/callback"
# Optional, only when the app has been approved for model-list access:
# export HEFU_OAUTH_SCOPE="ext_api ext_models:read"
# Optional current model ID for the final chat request:
export HEFU_MODEL="kimi-k3"
```

3. Install the dependency and start authorization:

```bash
pip install requests
python app-integration/oauth_pkce.py
```

4. Open the printed URL, review and approve the authorization, then copy the full callback URL:

```bash
python app-integration/oauth_pkce.py exchange "<full callback URL>"
```

The demo stores the PKCE verifier and expected state in `.hefu-oauth-session.json` with owner-only permissions, validates the returned state before exchanging the code, and removes the session after a successful exchange. The final chat request is real and billable to the authorizing user.

## Production checklist

- Store the PKCE verifier and expected state in the server-side session or an equivalent protected store, not in a browser-readable file.
- Use HTTPS callback URLs outside local development, validate the callback origin, and keep the state check.
- Request only the scopes your app needs. Available scopes and fields are defined in the [OpenAPI contract](https://hefu.hk/openapi.yaml).
- Store access and refresh tokens securely, honor expiry, and use the documented refresh-token grant when needed.
- Use bounded timeouts and retries; do not retry a rejected request blindly across every model.
- Show users when their HeFu balance is being used, and provide a way to revoke authorization.
