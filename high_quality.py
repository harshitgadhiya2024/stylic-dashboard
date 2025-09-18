import base64
from openai import OpenAI

try:
    client = OpenAI(api_key="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")

    pose_analysis_prompt = """
    POSE ANALYSIS REQUEST

    Analyze this image and provide a detailed description of the person's pose and body positioning ONLY. 

    IMPORTANT INSTRUCTIONS:
    - Focus EXCLUSIVELY on body positioning, stance, and pose
    - DO NOT describe clothing, garments, fabrics, colors, or fashion items
    - DO NOT describe background, setting, or environment
    - DO NOT describe facial features, hair, or accessories
    - Focus on: arm positions, leg positions, body angle, stance, posture, hand placement

    Provide a clear, detailed description of the pose that could be used to instruct a model to recreate the same body positioning.

    Example format: "Model standing with left hand on hip, right arm extended outward, weight shifted to right leg, head turned slightly to the left, confident upright posture"

    POSE DESCRIPTION:
    """

    # Generate content with image using GPT-4 Vision
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",  # or "gpt-4o" for the newer model
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": pose_analysis_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        max_tokens=500,
        temperature=0.3
    )

    if response and response.choices and response.choices[0].message.content:
        # Clean up the response to extract just the pose description
        pose_description = response.choices[0].message.content.strip()
        return pose_description

    return "Model in natural standing pose"

except Exception as e:
    print(f"Error analyzing pose from image: {str(e)}")
    return "Model in natural standing pose"