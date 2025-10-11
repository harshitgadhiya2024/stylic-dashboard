"""
AI Service - Integration with AI providers (OpenAI, Google AI, Anthropic)
"""
import os
import base64
from typing import Dict, Any, Optional, List
from PIL import Image
from io import BytesIO
import anthropic
import google.generativeai as genai
from app.core.config import settings
from app.core.logging import logger


class AIService:
    """Service for AI operations"""
    
    def __init__(self):
        """Initialize AI clients"""
        self.anthropic_client = None
        self.google_client = None
        
        # Initialize Anthropic client
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(
                api_key=settings.ANTHROPIC_API_KEY
            )
        
        # Initialize Google AI client
        if settings.GOOGLE_AI_API_KEY:
            genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
            self.google_client = genai
    
    async def analyze_pose_from_image(
        self,
        image_path: str
    ) -> str:
        """
        Analyze pose from an uploaded image using Claude
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Description of the pose detected in the image
        """
        try:
            if not self.anthropic_client:
                raise ValueError("Anthropic API key not configured")
            
            # Check if file exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Read and encode the image
            with open(image_path, "rb") as img_file:
                image_data = img_file.read()
                encoded_string = base64.b64encode(image_data).decode("utf-8")
            
            # Determine image format
            file_extension = os.path.splitext(image_path)[1].lower()
            media_type_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.webp': 'image/webp',
                '.gif': 'image/gif'
            }
            media_type = media_type_map.get(file_extension, 'image/jpeg')
            
            message = self.anthropic_client.messages.create(
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
- zoomed detail view (chest side garment detailing view)
- full body
- half back view upper body
- half lower body

Then provide a clear, detailed description of the pose that could be used to instruct a model to recreate the same body positioning.

Output format: "[View Type]: [Detailed pose description]"

Example: "half upper body front view: Model standing with left hand on hip, right arm extended outward, shoulders squared, head turned slightly to the left, confident upright posture with slight lean forward"

POSE DESCRIPTION:
"""
                            }
                        ]
                    }
                ]
            )
            
            pose_description = message.content[0].text
            logger.info(f"Pose analyzed from image: {image_path}")
            return pose_description
            
        except Exception as e:
            logger.error(f"Error analyzing pose from image: {str(e)}")
            raise
    
    async def generate_photoshoot_image(
        self,
        prompt: str,
        garment_images: List[str],
        background_image: Optional[str] = None,
        reference_image: Optional[str] = None
    ) -> bytes:
        """
        Generate photoshoot image using Google AI
        
        Args:
            prompt: Text prompt for image generation
            garment_images: List of garment image paths
            background_image: Optional background image path
            reference_image: Optional reference image for consistency
            
        Returns:
            Generated image as bytes
        """
        try:
            if not self.google_client:
                raise ValueError("Google AI API key not configured")
            
            model_gemini = "gemini-2.5-flash-image-preview"
            
            generate_content_config = types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"]
            )
            
            parts = []
            
            # Add garment images
            for garment_path in garment_images:
                if os.path.exists(garment_path):
                    with open(garment_path, "rb") as f:
                        image_data = f.read()
                    
                    exten = garment_path.split(".")[-1].lower()
                    if exten in ["jpg", "jpeg"]:
                        exten = "jpeg"
                    
                    parts.append(types.Part.from_bytes(
                        mime_type=f"image/{exten}",
                        data=image_data
                    ))
            
            # Add background image if provided
            if background_image and os.path.exists(background_image):
                with open(background_image, "rb") as f:
                    bg_data = f.read()
                parts.append(types.Part.from_bytes(
                    mime_type="image/webp",
                    data=bg_data
                ))
            
            # Add reference image if provided
            if reference_image and os.path.exists(reference_image):
                with open(reference_image, "rb") as f:
                    ref_data = f.read()
                parts.append(types.Part.from_bytes(
                    mime_type="image/png",
                    data=ref_data
                ))
            
            # Add text prompt
            parts.append(types.Part.from_text(text=prompt))
            
            contents = [
                types.Content(
                    role="user",
                    parts=parts
                )
            ]
            
            response = self.google_client.models.generate_content(
                model=model_gemini,
                contents=contents,
                config=generate_content_config
            )
            
            # Extract image from response
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    logger.info("Photoshoot image generated successfully")
                    return part.inline_data.data
            
            raise ValueError("No image generated in response")
            
        except Exception as e:
            logger.error(f"Error generating photoshoot image: {str(e)}")
            raise
    
    def calculate_estimated_cost(
        self,
        num_poses: int,
        has_upper_garment: bool = True,
        has_lower_garment: bool = True
    ) -> Dict[str, Any]:
        """
        Calculate estimated cost for photoshoot generation
        
        Args:
            num_poses: Number of poses to generate
            has_upper_garment: Whether upper garment is included
            has_lower_garment: Whether lower garment is included
            
        Returns:
            Cost estimation details
        """
        # Base costs per request
        text_input_cost_per_1k_tokens = 0.000075
        text_output_cost_per_1k_tokens = 0.0003
        image_input_cost = 0.00315
        estimated_image_generation_cost = 0.04
        
        # Estimate tokens per request
        avg_input_tokens = 500
        avg_output_tokens = 100
        
        # Calculate input images per request
        garment_images = (1 if has_upper_garment else 0) + (1 if has_lower_garment else 0)
        
        # Base request cost
        base_request_cost = (
            (avg_input_tokens * text_input_cost_per_1k_tokens / 1000) +
            (avg_output_tokens * text_output_cost_per_1k_tokens / 1000) +
            (garment_images * image_input_cost) +
            estimated_image_generation_cost
        )
        
        # Subsequent requests include reference image
        subsequent_request_cost = base_request_cost + image_input_cost
        
        # Total cost calculation
        if num_poses > 1:
            total_cost = base_request_cost + ((num_poses - 1) * subsequent_request_cost)
        else:
            total_cost = base_request_cost
        
        return {
            'total_requests': num_poses,
            'estimated_total_cost': round(total_cost, 4),
            'cost_per_image': round(total_cost / num_poses, 4),
            'base_request_cost': round(base_request_cost, 4),
            'subsequent_request_cost': round(subsequent_request_cost, 4)
        }


# Create singleton instance
ai_service = AIService()

