import json

from PIL import Image
import base64
import os
import anthropic


def analyze_pose_from_image(image_path, api_key="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"):
    """
    Analyze pose from an image using Claude Sonnet 4.

    Args:
        image_path (str): Path to the image file
        api_key (str, optional): Anthropic API key. If None, will try to get from environment

    Returns:
        str: Description of the pose detected in the image
    """
    try:
        # Get API key from environment if not provided
        if api_key is None:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("Anthropic API key not provided and ANTHROPIC_API_KEY environment variable not set")

        client = anthropic.Anthropic(api_key=api_key)

        # Check if file exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Read and encode the image
        with open(image_path, "rb") as img_file:
            image_data = img_file.read()
            encoded_string = base64.b64encode(image_data).decode("utf-8")

        # Determine image format from file extension
        file_extension = os.path.splitext(image_path)[1].lower()
        if file_extension in ['.jpg', '.jpeg']:
            media_type = "image/jpeg"
        elif file_extension == '.png':
            media_type = "image/png"
        elif file_extension == '.webp':
            media_type = "image/webp"
        elif file_extension == '.gif':
            media_type = "image/gif"
        else:
            # Default to jpeg for unknown formats
            media_type = "image/jpeg"

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": encoded_string
                            }
                        },
                        {
                            "type": "text",
                            "text": """POSE ANALYSIS REQUEST

                                Analyze this image and provide a detailed description of the person's pose and body positioning ONLY.

                                IMPORTANT INSTRUCTIONS:
                                - Focus EXCLUSIVELY on body positioning, stance, and pose
                                - DO NOT describe clothing, garments, fabrics, colors, or fashion items
                                - DO NOT describe background, setting, or environment
                                - DO NOT describe facial features, hair, or accessories
                                - Focus on: arm positions, leg positions, body angle, stance, posture, hand placement

                                First, identify the view type from these options:
                                - half upper body front view
                                - half side angle upper body
                                - zoomed detail view
                                - full body
                                - half Back view upper body

                                Then provide a clear, detailed description of the pose that could be used to instruct a model to recreate the same body positioning.

                                Output format: "[View Type]: [Detailed pose description]"

                                Example: "Half-upper-body: Model standing with left hand on hip, right arm extended outward, shoulders squared, head turned slightly to the left, confident upright posture with slight lean forward"

                                POSE DESCRIPTION:
                            """
                        }
                    ]
                }
            ]
        )

        pose_description = message.content[0].text

        # Clean up the response and validate
        if pose_description:
            pose_description = pose_description.strip()
            # print(f"Pose Analysis Result: {pose_description}")
            return pose_description
        else:
            print("No pose description returned from API")
            return "Model in natural standing pose"

    except FileNotFoundError as e:
        print(f"File error: {str(e)}")
        return "Model in natural standing pose"
    except ValueError as e:
        print(f"Configuration error: {str(e)}")
        return "Model in natural standing pose"
    except anthropic.APIError as e:
        print(f"Anthropic API error: {str(e)}")
        return "Model in natural standing pose"
    except Exception as e:
        print(f"Error analyzing pose from image: {str(e)}")
        return "Model in natural standing pose"

folder_path = "poses_photo"  # change this

# Get all files and directories
all_items = os.listdir(folder_path)

# Filter only files
files = [f for f in all_items if os.path.isfile(os.path.join(folder_path, f))]

print("Files in folder:")
all_file_dict = []
for file in files:
    image_path = f"poses_photo/{file}"
    pose_des = analyze_pose_from_image(image_path)
    print(pose_des)
    all_file_dict.append(pose_des)

with open("poses_data.json", "w") as f:
    json.dump(all_file_dict, f)