# # To run this code you need to install the following dependencies:
# # pip install google-genai
#
# import base64
# import mimetypes
# import os, uuid
#
# from PIL import Image
# from io import BytesIO
# from google import genai
# from google.genai import types
# from google.genai.types import MediaResolution
#
#
# def save_binary_file(file_name, data):
#     f = open(file_name, "wb")
#     f.write(data)
#     f.close()
#     print(f"File saved to to: {file_name}")
#
#
# def generate():
#     client = genai.Client(
#         api_key="AIzaSyBXyMioJM4k5YLKsYx6VkrZ6VSztsERC0w",
#     )
#
#     model = "gemini-2.5-flash-image-preview"
#     with open("garment.jpeg", "rb") as f:
#         image_data = f.read()
#
#     contents = [
#         types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_bytes(
#                     mime_type="image/jpeg",
#                     data=image_data,
#                 ),
#                 types.Part.from_text(text="""Could you please create a 5 images with different poses & background as given in below with 1 (25 years old indian male model) photoshoot for this kediyu and dhoti garment
#
# Replicate the EXACT full kediyu and dhoti garment from reference image - match fabric texture, color saturation, pattern details, fit precision, style elements and garment construction identically
#
# Background: plain white background
#
# pose1: A young dancer performing Garba, holding colorful dandiya sticks crossed above the head in a triumphant pose, one foot lifted gracefully, smiling joyfully
#
# pose2: A graceful Garba dancer mid-spin, holding dandiya sticks at waist level while rotating, one leg extended in dance position, radiant smile,
#
# pose3: A skilled Garba performer in a traditional squat position (bok step), holding dandiya sticks parallel to the ground, both hands extended sideways, knees bent in classic Garba stance, confident expression
#
# pose4: An energetic dancer captured mid-jump with both feet off the ground, dandiya sticks raised high in celebration, ecstatic expression of joy
#
# pose5: An elegant Garba dancer in a graceful side-step pose, holding dandiya sticks in an asymmetrical position - one high, one low, one leg extended to the side in perfect balance, serene focused expression
#
# - Ultra-high resolution (4K+), photorealistic quality
# - Professional fashion photography lighting with soft shadows
# - Precise fabric texture rendering and authentic draping
# - Color-accurate reproduction matching reference materials
# - Sharp focus on model and garments with depth of field
# - Professional model positioning and natural body language
# - Accurate garment length and silhouette representation
#
# Ensure perfect visual consistency while maintaining natural, realistic appearance and professional fashion photography standards.
# \""""),
#             ],
#         ),
#     ]
#     generate_content_config = types.GenerateContentConfig(
#         response_modalities=[
#             "IMAGE",
#             "TEXT",
#         ],
#     )
#
#     file_index = 0
#     for chunk in client.models.generate_content_stream(
#         model=model,
#         contents=contents,
#         config=generate_content_config,
#     ):
#         if (
#             chunk.candidates is None
#             or chunk.candidates[0].content is None
#             or chunk.candidates[0].content.parts is None
#         ):
#             continue
#         if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
#             file_name = f"output_{file_index}"
#             file_index += 1
#             inline_data = chunk.candidates[0].content.parts[0].inline_data
#             data_buffer = inline_data.data
#             file_extension = mimetypes.guess_extension(inline_data.mime_type)
#             save_binary_file(f"{file_name}{file_extension}", data_buffer)
#         else:
#             print(chunk.text)
#
# if __name__ == "__main__":
#     generate()


updated_list = []
for var in range(217):
    if var not in [182, 84, 184, 185, 186, 187]:
        updated_list.append(f"https://app.stylic.ai/static/generated_poses_new/pose_new_{var}.png.png")

print(updated_list)