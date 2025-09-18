from openai import OpenAI
import base64

# Path to your image
image_path = "input.png"

def analyze_pose_from_image(image_path, api_key="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"):
    client = OpenAI(api_key=api_key)

    # Read and encode the image
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode("utf-8")

    # Add the prefix for PNG
    data_uri = f"data:image/png;base64,{encoded_string}"

    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "POSE ANALYSIS REQUEST\n        \n        Analyze this image and provide a detailed description of the person's pose and body positioning ONLY. \n        \n        IMPORTANT INSTRUCTIONS:\n        - Focus EXCLUSIVELY on body positioning, stance, and pose\n        - DO NOT describe clothing, garments, fabrics, colors, or fashion items\n        - DO NOT describe background, setting, or environment\n        - DO NOT describe facial features, hair, or accessories\n        - Focus on: arm positions, leg positions, body angle, stance, posture, hand placement\n        \n        Provide a clear, detailed description of the pose that could be used to instruct a model to recreate the same body positioning.\n        \n        Example format: \"Model standing with left hand on hip, right arm extended outward, weight shifted to right leg, head turned slightly to the left, confident upright posture\"\n        \n        POSE DESCRIPTION:"
            },
            {
              "type": "image_url",
              "image_url": {
                "url": data_uri
              }
            }
          ]
        },
      ]
    )

    pose_description = response.choices[0].message.content
    print(pose_description)
    return pose_description

analyze_pose_from_image(image_path)

