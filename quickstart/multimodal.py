"""HeFu multimodal quickstart: explicitly selected image, audio or video calls.

Setup:
    pip install openai requests
    export HEFU_API_KEY="sk-hefu-..."
    python quickstart/multimodal.py --image
    python quickstart/multimodal.py --audio
    python quickstart/multimodal.py --video

Each option performs a real billable request. Optional model overrides:
HEFU_IMAGE_MODEL, HEFU_AUDIO_MODEL, HEFU_AUDIO_VOICE, HEFU_VIDEO_MODEL.
"""

import argparse
import os
import time

import requests
from openai import OpenAI

API_KEY = os.environ.get("HEFU_API_KEY")
BASE_URL = "https://api.hefu.hk/v1"


def pick_model(client: OpenAI, prefix: str) -> str | None:
    ids = [model.id for model in client.models.list().data]
    lowered = prefix.lower()
    return next((model_id for model_id in ids if model_id.lower().startswith(lowered)), None)


def generate_image(client: OpenAI) -> None:
    model = os.environ.get("HEFU_IMAGE_MODEL") or pick_model(client, "gpt-image") or pick_model(client, "dall-e")
    if not model:
        print("[image] no matching model; set HEFU_IMAGE_MODEL from the live catalog")
        return
    image = client.images.generate(
        model=model,
        prompt="A minimalist product shot of an API gateway hub, soft studio light",
        size="1024x1024",
        n=1,
    )
    print(f"[image] model={model} url={image.data[0].url}")


def generate_speech(client: OpenAI) -> None:
    model = os.environ.get("HEFU_AUDIO_MODEL") or next(
        (model_id for prefix in ("speech", "tts", "minimax", "kokoro") if (model_id := pick_model(client, prefix))),
        None,
    )
    if not model:
        print("[audio] no matching model; set HEFU_AUDIO_MODEL from the live catalog")
        return
    voice = os.environ.get("HEFU_AUDIO_VOICE", "alloy")
    speech = client.audio.speech.create(
        model=model,
        voice=voice,
        input="HeFu provides a unified model API for developers.",
    )
    speech.stream_to_file("hefu-intro.mp3")
    print(f"[audio] model={model} voice={voice} saved hefu-intro.mp3")


def generate_video() -> None:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    model = os.environ.get("HEFU_VIDEO_MODEL")
    if not model:
        raise SystemExit("Set HEFU_VIDEO_MODEL to a current video model ID; video calls are billable")

    submit = requests.post(
        f"{BASE_URL}/videos/generations",
        headers=headers,
        json={
            "model": model,
            "prompt": "Slow zoom-in on a glowing network hub over Hong Kong harbour at dusk",
        },
        timeout=120,
    )
    submit.raise_for_status()
    job = submit.json()
    job_id = job.get("id") or (job.get("data") or {}).get("id")
    if not job_id:
        raise RuntimeError(f"Video response has no job id: {job}")
    print(f"[video] job submitted: id={job_id}")

    deadline = time.time() + 600
    while time.time() < deadline:
        response = requests.get(
            f"{BASE_URL}/videos/generations/{job_id}",
            headers=headers,
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        status = payload.get("status") or (payload.get("data") or {}).get("status")
        legacy = payload.get("status_legacy")
        print(f"[video] status={status or legacy}")
        if status == "completed" or legacy in ("succeeded", "success", "done"):
            url = payload.get("video_url") or payload.get("url") or (payload.get("data") or {}).get("url")
            print(f"[video] done: {url}")
            return
        if status == "failed" or legacy in ("failed", "error", "cancelled"):
            raise RuntimeError(f"Video generation failed: {payload}")
        time.sleep(10)
    raise TimeoutError("Video job is still running; use the job id to check it later")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", action="store_true", help="generate one billable image")
    parser.add_argument("--audio", action="store_true", help="generate one billable audio file")
    parser.add_argument("--video", action="store_true", help="submit and poll one billable video job")
    args = parser.parse_args()
    if not (args.image or args.audio or args.video):
        parser.print_help()
        raise SystemExit(2)
    if not API_KEY:
        raise SystemExit("HEFU_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    if args.image:
        generate_image(client)
    if args.audio:
        generate_speech(client)
    if args.video:
        generate_video()


if __name__ == "__main__":
    main()
