import time
import os
from openai import OpenAI
import base64

from utils.constant import constant_dict

# Create output directory
output_dir = "generated_poses"
os.makedirs(output_dir, exist_ok=True)

# Your 30 pose prompts
fashion_poses = [
    "Model standing straight, facing camera, hands on hips, confident look, full outfit in view",
    "Model in relaxed stance, one leg slightly forward, arms crossed, looking to side",
    "Model standing with one arm raised, leaning slightly back, dramatic lighting",
    "Model walking forward, mid-stride, natural motion, wind in hair or fabric",
    "Model standing sideways, looking over shoulder, showing side profile and outfit shape",
    "Model leaning slightly on wall, hands in pockets, casual expression",
    "Model with arms crossed behind back, clean backdrop, neutral lighting",
    "Model holding a handbag with one hand, other hand on waist, urban background",
    "Model adjusting sunglasses or collar, slightly looking down, fashion-forward angle",
    "Model standing on one leg with the other bent, playful posture, vibrant mood",
    "Model sitting on stool, one leg crossed over the other, hands on lap, straight back",
    "Model leaning forward on knees, elbows on thighs, intense eye contact",
    "Model lounging on couch, legs extended, arm behind head, relaxed elegance",
    "Model sitting sideways on stairs, chin resting on hand, urban style",
    "Model sitting cross-legged on floor, looking up slightly, natural pose",
    "Model seated on high chair, legs crossed, arms resting casually, studio backdrop",
    "Model with one knee up, seated on step, elbows resting on knee, thoughtful look",
    "Model reclining slightly on floor with one arm supporting upper body, full outfit visible",
    "Model sitting on window ledge, sunlight hitting face, casual urban vibe",
    "Model sitting backwards on chair, arms resting on backrest, bold streetwear pose",
    "Model in high-fashion stance, one foot forward, hips tilted, dramatic pose with shadows",
    "Model holding flowing fabric in motion, elegant long dress, wind effect",
    "Model in asymmetrical pose, arm lifted, intense makeup and styling",
    "Model in power pose, hands on waist, wide-legged stance, blazer and heels",
    "Model leaning dramatically to side, high contrast lighting, editorial look",
    "Model crouching low with head turned toward camera, street style outfit",
    "Model posing with garment in motion, twirling or flipping skirt, studio setup",
    "Model with arms spread out, coat open wide, walking with confidence",
    "Model using accessory as a prop (hat, handbag), interacting naturally with it",
    "Model gazing over sunglasses, strong jawline highlighted, glossy backdrop"
]

for i, prompt in enumerate(fashion_poses, start=1):
    print(f"Generating realistic human model image for pose {i}...")
    try:
        prompt = f"Generating realistic human model image for pose {prompt}"
        client = OpenAI(
            api_key=constant_dict.get("openai_key"))

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        # Save the image to a file
        with open(f"generated_poses/pose_new_{i}.png", "wb") as f:
            f.write(image_bytes)
        print(f"✅ Saved: generated_poses/pose_new_{i}.png")
    except Exception as e:
        print(f"❌ Error on pose {i}: {e}")

    # Optional: avoid rate limits
    time.sleep(2)
