"""HeFu third-party app integration with OAuth + PKCE (public client, no secret).

The HeFu developer platform (https://www.hefu.hk/docs) supports a zero-cost
integration model: your app redirects users through HeFu OAuth, the *user* pays
for their own model usage, and your app never holds an API key or a client
secret. Public clients skip secret validation entirely — PKCE (RFC 7636/8252)
is enforced instead.

Flow:
    1. Build an authorize URL with a PKCE S256 challenge and send the user there.
    2. HeFu authenticates the user and redirects back with an authorization `code`.
    3. Exchange the code (+ original code_verifier, no secret) for tokens.
    4. Call https://api.hefu.hk/v1/* with the user's access token.

Setup:
    pip install requests
    export HEFU_CLIENT_ID="..."   # register your app in the HeFu console, see /docs
    export HEFU_REDIRECT_URI="http://localhost:8000/callback"
    python app-integration/oauth_pkce.py        # prints the authorize URL, then:
    python app-integration/oauth_pkce.py exchange <code>
"""

import base64
import hashlib
import os
import secrets
import sys
import urllib.parse

import requests

AUTHORIZE_URL = "https://hefu.hk/api/v1/oauth/authorize"
TOKEN_URL = "https://api.hefu.hk/v1/oauth/token"
API_BASE = "https://api.hefu.hk/v1"

CLIENT_ID = os.environ.get("HEFU_CLIENT_ID")
REDIRECT_URI = os.environ.get("HEFU_REDIRECT_URI", "http://localhost:8000/callback")
# Public scope list; adjust to what your app registered. "model:invoke" style
# scopes are documented on https://www.hefu.hk/docs — start minimal.
SCOPE = os.environ.get("HEFU_OAUTH_SCOPE", "openid profile")


def new_pkce_pair() -> tuple[str, str]:
    """Return (code_verifier, code_challenge) using S256."""
    verifier = secrets.token_urlsafe(64)[:96]  # 43-128 chars per RFC 7636
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


def authorize_url() -> tuple[str, str]:
    """Print the URL to open in the browser; returns (url, code_verifier)."""
    if not CLIENT_ID:
        raise SystemExit("HEFU_CLIENT_ID is not set. Register your app per https://www.hefu.hk/docs")
    verifier, challenge = new_pkce_pair()
    query = urllib.parse.urlencode(
        {
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": SCOPE,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        }
    )
    return f"{AUTHORIZE_URL}?{query}", verifier


def exchange_code(code: str, verifier: str) -> dict:
    """Exchange the authorization code for tokens. No client_secret is sent."""
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "code_verifier": verifier,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def call_with_user_token(access_token: str) -> None:
    """Example: a chat completion billed to the *user's* HeFu balance."""
    resp = requests.post(
        f"{API_BASE}/chat/completions",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "model": "kimi-k3",  # resolve the live id from GET /v1/models
            "messages": [{"role": "user", "content": "Say hello in five words."}],
        },
        timeout=120,  # the gateway recommends >=120s client timeouts; streaming is unaffected
    )
    resp.raise_for_status()
    print(resp.json()["choices"][0]["message"]["content"])


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "exchange":
        # Usage: exchange <code>  (paste the ?code=... from the redirect URI)
        # The verifier is re-derived in real apps via session storage; for this
        # demo run the script once to get the URL, keep the printed verifier,
        # then exchange. A production app should store the verifier server-side.
        print("NOTE: keep the code_verifier printed in step 1 and pass it here.")
        _, code, verifier = sys.argv[0], sys.argv[2], sys.argv[3]
        tokens = exchange_code(code, verifier)
        print("tokens:", {k: (v[:20] + "...") if isinstance(v, str) and len(v) > 24 else v for k, v in tokens.items()})
        call_with_user_token(tokens["access_token"])
    else:
        url, verifier = authorize_url()
        print("1. Open this URL in the browser and approve the app:")
        print(url)
        print()
        print("2. After approval you are redirected to:")
        print(f"   {REDIRECT_URI}?code=...&state=...")
        print("3. Save this code_verifier (needed for the exchange step):")
        print(verifier)
        print()
        print("4. Exchange:")
        print(f"   python app-integration/oauth_pkce.py exchange <code> {verifier}")
