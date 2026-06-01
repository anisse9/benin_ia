"""
GÃ©nÃ¨re une vidÃ©o 5s avec Kling (Fal.ai) depuis l'image usecase-detection-maladies-cultures.png
et la place dans AGRIBOT/assets/hero-agribot.mp4
"""

import fal_client
import base64, os, urllib.request

IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "usecase-detection-maladies-cultures.png")
OUT_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AGRIBOT", "assets")
OUT_PATH   = os.path.join(OUT_DIR, "hero-agribot.mp4")

PROMPT = (
    "A realistic farmer gently lifts the corn leaf away from the phone, holds the leaf "
    "still while taking a photo, then carefully places the leaf back in its original "
    "position. Keep the original composition and camera angle stable. Realistic hand "
    "motion, natural body movement, subtle wind in the leaves, no scene change, no object "
    "passing through the phone, no deformation, no extra motion. Then the farmer turns "
    "toward the camera, smiles, and gives a clear thumbs-up gesture. Preserve the same "
    "environment, realistic physics, subtle motion only, cinematic but natural, no warping."
)

def image_to_data_uri(path: str) -> str:
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("Envoi de l'image Ã  Fal.ai (Kling image-to-video 1.6)â€¦")
    data_uri = image_to_data_uri(IMAGE_PATH)

    result = fal_client.subscribe(
        "fal-ai/kling-video/v1.6/standard/image-to-video",
        arguments={
            "image_url": data_uri,
            "prompt": PROMPT,
            "duration": "5",
            "aspect_ratio": "16:9",
            "negative_prompt": "blur, low quality, deformed, extra people, text overlay, watermark",
            "cfg_scale": 0.5,
        },
        with_logs=True,
        on_queue_update=lambda u: print(f"  [{u.status}]" if hasattr(u, "status") else f"  log: {u}"),
    )

    video_url = result["video"]["url"]
    print(f"\nVidÃ©o gÃ©nÃ©rÃ©e : {video_url}")
    print(f"TÃ©lÃ©chargement â†’ {OUT_PATH}")
    urllib.request.urlretrieve(video_url, OUT_PATH)
    print("TerminÃ©.")

if __name__ == "__main__":
    main()


