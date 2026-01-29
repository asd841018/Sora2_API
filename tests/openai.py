from PIL import Image, ImageOps
from pathlib import Path
import openai
import time
import requests

SORA_RESOLUTIONS = {
    "landscape_720p": (1280, 720),
    "portrait_720p": (720, 1280),
    "landscape_1080p": (1792, 1024),
    "portrait_1080p": (1024, 1792),
}

def preprocess_image_for_sora(image_path, target_resolution="landscape_720p"):
    target_size = SORA_RESOLUTIONS[target_resolution]

    img = Image.open(image_path)

    processed = ImageOps.pad(img, target_size, color=(0, 0, 0))

    output_path = image_path.replace(".png", "_sora_ready.png")
    processed.save(output_path)

    return output_path

openai.api_key = ""

def generate_sora_video(prompt_description, image_path):
    """Generates a video using the Sora 2 API and downloads it."""
    try:
        print(f"Sending video generation request for prompt: '{prompt_description}'")
        processed_image = preprocess_image_for_sora(image_path, "portrait_720p")
        img_path = Path(processed_image)
        # 1. Send request to create video
        response = openai.videos.create(
            model="sora-2",  # Specify the model
            prompt=prompt_description,
            size="720x1280", # Optional: landscape resolution
            seconds="8",       # Optional: clip duration (4, 8, or 12 allowed)
            input_reference=img_path
        )

        video_id = response.id
        print(f"Video generation job started with ID: {video_id}. Waiting for completion...")

        # 2. Poll for video status until complete
        while True:
            status_response = openai.videos.retrieve(video_id)
            if status_response.status == "completed":
                print(f"Video generated successfully. Download video: {video_id}")
                # 3. Download the generated video
                content = openai.videos.download_content(video_id, variant="video")
                content.write_to_file("video.mp4")
                break
            elif status_response.status == "failed":
                print(f"Video generation failed: {status_response.error}")
                break
            else:
                print("Video still processing, checking again in 10 seconds...")
                time.sleep(10)

    except Exception as e:
        print(f"An error occurred: {e}")


# Example Usage
# For best results, use detailed prompts describing shot type, subject, action, setting, and lighting.
prompt_example = "The girl holding her coffee and walking on the street in autumn"
image_path_example = "D:/work/Sora2_API/probe.png"

generate_sora_video(prompt_example, image_path_example)