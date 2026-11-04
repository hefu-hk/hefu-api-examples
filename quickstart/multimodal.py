"""HeFu multimodal quickstart: images, audio and video through one API key.

HeFu covers text, image, video and voice models behind a single OpenAI-compatible
endpoint. This script shows the three non-text surfaces with the same key and
base URL you already use for chat.

Setup:
    pip install openai requests
    export HEFU_API_KEY="sk-hefu-..."
    python quickstart/multimodal.py

Model IDs change over time — always resolve them dynamically from /v1/models
(the script does this) or check https://www.hefu.hk/models for the live catalog
(as of 2026-11).
"""

import os
import time

import requests
from openai import OpenAI

API_KEY = os.environ.get("HEFU_API_KEY")
if not API_KEY:
    raise SystemExit("HEFU_API_KEY is not set. Export it first, e.g.: export HEFU_API_KEY=sk-hefu-...")

BASE_URL = "https://api.hefu.hk/v1"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def pick_model(prefix: str) -> str | None:
    """Return the first available model id that starts with `prefix`."""
    ids = [m.id for m in client.models.list().data]
    return next((i for i in ids if i.startswith(prefix)), None)


# ---------------------------------------------------------------- images ----
image_model = pick_model("gpt-image") or pick_model("dall-e")
if image_model:
    image = client.images.generate(
        model=image_model,
        prompt="A minimalist product shot of an API gateway hub, soft studio light",
        size="1024x1024",
        n=1,
    )
    print(f"[image] model={image_model} url={image.data[0].url}")
else:
    print("[image] no image model id matched the known prefixes; list /v1/models and adjust")

# ---------------------------------------------------------------- audio -----
audio_model = pick_model("speech") or pick_model("tts") or pick_model("MiniMax")
if audio_model:
    speech = client.audio.speech.create(
        model=audio_model,
        voice="alloy",  # voice catalog varies by model; see https://www.hefu.hk/docs
        input="HeFu is an AI API aggregation platform. One key, every model.",
    )
    speech.stream_to_file("hefu-intro.mp3")
    print(f"[audio] model={audio_model} saved hefu-intro.mp3")
else:
    print("[audio] no speech model id matched the known prefixes; list /v1/models and adjust")

# ---------------------------------------------------------------- video -----
# Video generation is asynchronous: submit a job, then poll until it finishes.
video_model = pick_model("kling") or pick_model("vidu")
if video_model:
    submit = requests.post(
        f"{BASE_URL}/videos/generations",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": video_model,
            "prompt": "Slow zoom-in on a glowing network hub over Hong Kong harbour at dusk",
            # seconds/size parameters differ per model; see the OpenAPI contract:
            # https://hefu.hk/openapi.yaml
        },
        timeout=120,
    )
    submit.raise_for_status()
    job = submit.json()
    job_id = job.get("id") or (job.get("data") or {}).get("id")
    print(f"[video] job submitted: id={job_id}")

    deadline = time.time() + 600  # poll up to 10 minutes
    while time.time() < deadline:
        status_resp = requests.get(
            f"{BASE_URL}/videos/generations/{job_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=60,
        )
        status_resp.raise_for_status()
        payload = status_resp.json()
        status = payload.get("status") or (payload.get("data") or {}).get("status")
        print(f"[video] status={status}")
        if status in ("succeeded", "success", "completed", "done"):
            url = payload.get("url") or payload.get("video_url") or (payload.get("data") or {}).get("url")
            print(f"[video] done: {url}")
            break
        if status in ("failed", "error", "cancelled"):
            print(f"[video] failed: {payload}")
            break
        time.sleep(10)
else:
    print("[video] no video model id matched the known prefixes; list /v1/models and adjust")
