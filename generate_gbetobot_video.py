"""
Génère une vidéo 10s avec Kling (Fal.ai) depuis l'image gbetobot-renouvellement-passeport.png
et la place dans GBETOBOT/assets/hero-gbetobot.mp4
"""

import os, base64, urllib.request

# Lecture de la clé depuis .env
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
_fal_key = ""
if os.path.exists(_env_path):
    with open(_env_path, encoding="utf-8-sig") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line.startswith("FAL_KEY="):
                _fal_key = _line.split("=", 1)[1].strip()
                break

if not _fal_key:
    raise SystemExit("FAL_KEY introuvable dans .env")

import fal_client

# Instanciation du client avec la clé passée directement — bypass fetch_auth_credentials()
client = fal_client.SyncClient(key=_fal_key)

IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gbetobot-renouvellement-passeport.png")
OUT_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GBETOBOT", "assets")
OUT_PATH   = os.path.join(OUT_DIR, "hero-gbetobot.mp4")

PROMPT = (
    "The young man slowly lifts his gaze from the passport he is holding, studying it carefully. "
    "He then reaches into his pocket and picks up his smartphone with his other hand. "
    "He glances at the phone screen — a WhatsApp conversation is visible — "
    "then he raises his eyes toward the camera, a warm and confident smile spreading across his face. "
    "He holds up his open passport toward the camera, showing it proudly. "
    "There is a plain white ceramic mug on the desk beside the laptop. "
    "Soft natural indoor light. Cinematic, calm and confident, shallow depth of field, "
    "warm neutral tones. No text overlay, no subtitles. "
    "Keep the original composition and camera angle stable. Realistic motion, no warping, no deformation."
)

def image_to_data_uri(path: str) -> str:
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"Clé FAL chargée : {_fal_key[:12]}…")
    print("Envoi de l'image à Fal.ai (Kling image-to-video 1.6)…")
    data_uri = image_to_data_uri(IMAGE_PATH)

    result = client.subscribe(
        "fal-ai/kling-video/v1.6/standard/image-to-video",
        arguments={
            "image_url": data_uri,
            "prompt": PROMPT,
            "duration": "10",
            "aspect_ratio": "16:9",
            "negative_prompt": "blur, low quality, deformed, extra people, text overlay, watermark, camera movement, yellow mug, colored mug, orange mug",
            "cfg_scale": 0.5,
        },
        with_logs=True,
        on_queue_update=lambda u: print(f"  [{u.status}]" if hasattr(u, "status") else f"  log: {u}"),
    )

    video_url = result["video"]["url"]
    print(f"\nVidéo générée : {video_url}")
    print(f"Téléchargement → {OUT_PATH}")
    urllib.request.urlretrieve(video_url, OUT_PATH)
    print("Terminé.")

if __name__ == "__main__":
    main()
