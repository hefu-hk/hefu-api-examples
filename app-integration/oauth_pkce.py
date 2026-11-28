"""HeFu third-party app integration with OAuth 2.0, PKCE and state validation.

Setup:
    pip install requests
    export HEFU_CLIENT_ID="..."
    export HEFU_REDIRECT_URI="http://localhost:8000/callback"
    python app-integration/oauth_pkce.py
    python app-integration/oauth_pkce.py exchange "<full callback URL>"

The demo stores the verifier and expected state in a local 0600 file between
steps. Production apps should use their server-side session instead.
"""

import base64
import hashlib
import json
import os
import secrets
import sys
import urllib.parse
from pathlib import Path

import requests

AUTHORIZE_URL = "https://hefu.hk/oauth/authorize"
TOKEN_URL = "https://api.hefu.hk/api/v1/oauth/token"
CHAT_URL = "https://api.hefu.hk/api/v1/ext/chat/completions"
SESSION_PATH = Path(".hefu-oauth-session.json")

CLIENT_ID = os.environ.get("HEFU_CLIENT_ID")
REDIRECT_URI = os.environ.get("HEFU_REDIRECT_URI", "http://localhost:8000/callback")
SCOPE = os.environ.get("HEFU_OAUTH_SCOPE", "ext_api")
MODEL = os.environ.get("HEFU_MODEL", "deepseek-v4-flash")


def new_pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)[:96]
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


def authorize_url() -> tuple[str, str, str]:
    if not CLIENT_ID:
        raise SystemExit("HEFU_CLIENT_ID is not set. Register your app per https://hefu.hk/docs")
    verifier, challenge = new_pkce_pair()
    state = secrets.token_urlsafe(24)
    query = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    })
    return f"{AUTHORIZE_URL}?{query}", verifier, state


def save_session(verifier: str, state: str) -> None:
    payload = json.dumps({"verifier": verifier, "state": state})
    fd = os.open(SESSION_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, "w") as handle:
        handle.write(payload)


def exchange_code(callback_url: str) -> dict:
    try:
        session = json.loads(SESSION_PATH.read_text())
    except (OSError, ValueError) as exc:
        raise SystemExit("Run the authorize step first; no valid OAuth session was found") from exc

    params = urllib.parse.parse_qs(urllib.parse.urlparse(callback_url).query)
    code = params.get("code", [""])[0]
    returned_state = params.get("state", [""])[0]
    if not code:
        raise SystemExit("The callback URL does not contain an authorization code")
    if not returned_state or not secrets.compare_digest(returned_state, session["state"]):
        raise SystemExit("OAuth state mismatch; do not exchange this callback")

    resp = requests.post(
        TOKEN_URL,
        json={
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "code_verifier": session["verifier"],
        },
        timeout=60,
    )
    resp.raise_for_status()
    SESSION_PATH.unlink(missing_ok=True)
    return resp.json()


def call_with_user_token(access_token: str) -> None:
    resp = requests.post(
        CHAT_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": "Say hello in five words."}],
        },
        timeout=120,
    )
    resp.raise_for_status()
    print(resp.json()["choices"][0]["message"]["content"])


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "exchange":
        if len(sys.argv) != 3:
            raise SystemExit('Usage: python app-integration/oauth_pkce.py exchange "<full callback URL>"')
        tokens = exchange_code(sys.argv[2])
        print("token fields:", sorted(tokens))
        call_with_user_token(tokens["access_token"])
    else:
        url, verifier, state = authorize_url()
        save_session(verifier, state)
        print("1. Open this URL and approve the app:")
        print(url)
        print("\n2. Copy the full callback URL after approval, then run:")
        print('   python app-integration/oauth_pkce.py exchange "<full callback URL>"')
        print(f"\nOAuth session saved to {SESSION_PATH} with owner-only permissions.")
