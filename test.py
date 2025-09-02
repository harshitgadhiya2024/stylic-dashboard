# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import mimetypes
import os, uuid

from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types
from google.genai.types import MediaResolution


def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    print(f"File saved to to: {file_name}")


def generate():
    client = genai.Client(
        api_key="AIzaSyBXyMioJM4k5YLKsYx6VkrZ6VSztsERC0w",
    )

    model = "gemini-2.5-flash-image-preview"
    with open("garment.png", "rb") as f:
        image_data = f.read()

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(
                    mime_type="image/png",
                    data=image_data,
                ),
                types.Part.from_text(text="""
                    Could you please create a model photoshoot for given all poses with this given garment
                    
                    Replicate the EXACT garment from reference image - match fabric texture, color saturation, pattern details in whole garment, fit precision, style elements, Clearly shows: Button detailing and garment construction identically
                    
                    Human model age: 25 years (Indian)
                    GARMENT FITTING: regular fit
                    total need to generate image (each pose has seperate image): 3
                    
                    pose1: Model seated on high chair, legs crossed, arms resting casually, studio backdrop
                    pose2: Model sitting on window ledge, sunlight hitting face, casual urban vibe
                    pose3: Model sitting backwards on chair, arms resting on backrest, bold streetwear pose
                    
                    TECHNICAL SPECIFICATIONS:
                    
                    - Ultra-high resolution (4K+), **specifically 2160x3840 pixels**, photorealistic quality
                    - **Aspect ratio: 9:16 (vertical)**
                    - Professional fashion photography lighting with soft shadows
                    - Precise fabric texture rendering and authentic draping
                    - Color-accurate reproduction matching reference materials
                    - Sharp focus on model and garments with depth of field
                    - Professional model positioning and natural body language
                    - Accurate garment length and silhouette representation
                    
                    Ensure perfect visual consistency while maintaining natural, realistic appearance and professional fashion photography standards.
                """),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_modalities=[
            "IMAGE",
            "TEXT",
        ],
        media_resolution=MediaResolution.MEDIA_RESOLUTION_HIGH
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=contents,
        config=generate_content_config
    )
    file_index = 0
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            file_index += 1
            image = Image.open(BytesIO(part.inline_data.data))
            filename = f"generated_image_{uuid.uuid4()}.png"
            image.save(filename)


if __name__ == "__main__":
    generate()
