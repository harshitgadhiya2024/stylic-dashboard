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
                                - half left side angle upper body
                                - half right side angle upper body
                                - zoomed detail view zoomed detailing view (chest side garment detailing view - when the photo is zoomed in to focus on upper chest/torso area for garment details)
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
            print(f"Pose Analysis Result: {pose_description}")
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

def analyze_multiple_pose_images(image_files):
    """
    Analyze multiple pose images and return pose descriptions.
    
    Args:
        image_files: List of image file paths or bytes
        api_key: Google AI API key
        
    Returns:
        list: List of pose descriptions
    """
    pose_descriptions = []
    
    for i, image_file in enumerate(image_files):
        try:
            pose_desc = analyze_pose_from_image(image_file)
            pose_descriptions.append(pose_desc)
            print(f"Analyzed pose {i+1}/{len(image_files)}: {pose_desc[:100]}...")
        except Exception as e:
            print(f"Error analyzing pose image {i+1}: {str(e)}")
            pose_descriptions.append(f"Model in natural pose {i+1}")
    
    return pose_descriptions


def save_uploaded_pose_images(uploaded_files, photoshoot_id):
    """
    Save uploaded pose images to the photoshoot folder.
    
    Args:
        uploaded_files: List of uploaded file objects
        photoshoot_id: Unique photoshoot ID
        
    Returns:
        list: List of saved file paths
    """
    saved_paths = []
    pose_folder = f"static/photoshoots_folders/{photoshoot_id}/poses"
    os.makedirs(pose_folder, exist_ok=True)
    
    for i, file in enumerate(uploaded_files):
        if file and file.filename:
            # Generate unique filename
            file_extension = file.filename.split('.')[-1].lower()
            filename = f"pose_{i+1}.{file_extension}"
            filepath = os.path.join(pose_folder, filename)
            
            # Save file
            file.save(filepath)
            saved_paths.append(filepath)
    
    return saved_paths


def validate_pose_image(image_file):
    """
    Validate if uploaded file is a valid image.
    
    Args:
        image_file: Uploaded file object
        
    Returns:
        bool: True if valid image, False otherwise
    """
    try:
        if not image_file or not image_file.filename:
            return False
            
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        file_extension = image_file.filename.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            return False
            
        # Try to open with PIL to validate it's a real image
        image_file.seek(0)  # Reset file pointer
        image = Image.open(image_file)
        image.verify()  # Verify it's a valid image
        image_file.seek(0)  # Reset file pointer again
        
        return True
        
    except Exception as e:
        print(f"Image validation error: {str(e)}")
        return False
