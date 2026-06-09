"""
Génère une vidéo 8s avec Kling (Fal.ai) depuis l'image detection-asphyxie-pleurs-smartphone.png
et la place dans ASPHYXIABOT/assets/hero-asphyxiabot.mp4
"""

import fal_client
import base64, os, urllib.request

# Chargement de la clé API depuis .env
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ[_k.strip()] = _v.strip()

fal_client.api_key = os.environ.get("FAL_KEY", "")

IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "detection-asphyxie-pleurs-smartphone.png")
OUT_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ASPHYXIABOT", "assets")
OUT_PATH   = os.path.join(OUT_DIR, "hero-asphyxiabot.mp4")

PROMPT = (
    "The young mother gently rocks the crying newborn in her arms, softly swaying side to side. "
    "She holds her smartphone close to the baby's mouth, recording the cry. "
    "The phone screen glows with a green audio waveform pulsing to the baby's sounds. "
    "After a few seconds, the mother glances at the phone screen — a result appears — "
    "she slowly lifts her gaze toward the camera and a warm, relieved smile spreads across her face. "
    "Soft natural light from the window. Cinematic, slow and intimate, shallow depth of field, "
    "warm golden tones. No text overlay, no subtitles. "
    "Keep the original composition and camera angle stable. Realistic motion, no warping, no deformation."
)

def image_to_data_uri(path: str) -> str:
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("Envoi de l'image à Fal.ai (Kling image-to-video 1.6)…")
    data_uri = image_to_data_uri(IMAGE_PATH)

    result = fal_client.subscribe(
        "fal-ai/kling-video/v1.6/standard/image-to-video",
        arguments={
            "image_url": data_uri,
            "prompt": PROMPT,
            "duration": "10",
            "aspect_ratio": "16:9",
            "negative_prompt": "blur, low quality, deformed, extra people, text overlay, watermark, camera movement",
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
