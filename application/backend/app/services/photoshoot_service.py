"""
Photoshoot Service - Business logic for photoshoot operations
"""
import os
import uuid
import subprocess
from typing import Dict, Any, List, Optional
from datetime import datetime
from PIL import Image
from io import BytesIO
from app.services.mongo_service import mongo_service
from app.services.ai_service import ai_service
from app.core.config import settings
from app.core.logging import logger


class PhotoshootService:
    """Service for photoshoot operations"""
    
    def __init__(self):
        """Initialize photoshoot service"""
        self.upload_dir = settings.UPLOAD_DIR
        self.predefined_poses = self._load_predefined_poses()
    
    def _load_predefined_poses(self) -> List[str]:
        """Load predefined pose descriptions"""
        # This is a subset - full list in ai_photoshoot_generation.py
        return [
            "full body standing straight facing camera, hands on hips, confident look",
            "full body relaxed stance, one leg slightly forward, arms crossed, looking to side",
            "full body standing with one arm raised, leaning slightly back",
            "full body walking forward mid-stride, natural motion",
            "half right side angle upper body standing sideways, looking over shoulder",
            "full body leaning slightly on wall, hands in pockets",
            "full body arms crossed behind back",
            "full body one hand on waist",
            "half upper body front view slightly looking down",
            "full body standing on one leg with the other bent, playful posture",
        ]
    
    async def create_photoshoot(
        self,
        user_id: str,
        photoshoot_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new photoshoot
        
        Args:
            user_id: User ID
            photoshoot_data: Photoshoot configuration
            
        Returns:
            Created photoshoot details
        """
        try:
            photoshoot_id = str(uuid.uuid4())
            
            # Create photoshoot directory
            photoshoot_dir = os.path.join(
                self.upload_dir,
                "photoshoots",
                photoshoot_id
            )
            os.makedirs(photoshoot_dir, exist_ok=True)
            
            # Prepare photoshoot record
            photoshoot_record = {
                "id": user_id,
                "photoshoot_id": photoshoot_id,
                "upload_garment_type": photoshoot_data.get("garment_type"),
                "age_group": photoshoot_data.get("age_group"),
                "gender": photoshoot_data.get("gender"),
                "ethnicity": photoshoot_data.get("ethnicity"),
                "height": photoshoot_data.get("height"),
                "weight": photoshoot_data.get("weight"),
                "age": photoshoot_data.get("age"),
                "fitting": photoshoot_data.get("fitting"),
                "background_description": photoshoot_data.get("background_description"),
                "selected_background": photoshoot_data.get("selected_background"),
                "pose_input_method": photoshoot_data.get("pose_input_method", "predefined"),
                "selected_poses": photoshoot_data.get("selected_poses", []),
                "pose_descriptions": photoshoot_data.get("pose_descriptions", []),
                "upper_garment_specs": photoshoot_data.get("upper_garment_specs"),
                "lower_garment_specs": photoshoot_data.get("lower_garment_specs"),
                "all_images": [],
                "total_credit": 0,
                "is_credit_debited": False,
                "is_completed": False,
                "status": "pending",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Insert into database
            await mongo_service.insert_one("photoshoot_data", photoshoot_record)
            
            logger.info(f"Photoshoot created: {photoshoot_id} for user: {user_id}")
            
            return {
                "photoshoot_id": photoshoot_id,
                "status": "pending",
                "message": "Photoshoot created successfully"
            }
            
        except Exception as e:
            logger.error(f"Error creating photoshoot: {str(e)}")
            raise
    
    async def process_pose_images(
        self,
        pose_images: List[str],
        photoshoot_id: str
    ) -> List[str]:
        """
        Process uploaded pose images and extract pose descriptions
        
        Args:
            pose_images: List of pose image paths
            photoshoot_id: Photoshoot ID
            
        Returns:
            List of pose descriptions
        """
        try:
            pose_descriptions = []
            
            for image_path in pose_images:
                # Analyze pose using AI
                description = await ai_service.analyze_pose_from_image(image_path)
                pose_descriptions.append(description)
            
            logger.info(f"Processed {len(pose_images)} pose images for photoshoot: {photoshoot_id}")
            return pose_descriptions
            
        except Exception as e:
            logger.error(f"Error processing pose images: {str(e)}")
            raise
    
    async def get_photoshoot(
        self,
        user_id: str,
        photoshoot_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get photoshoot details
        
        Args:
            user_id: User ID
            photoshoot_id: Photoshoot ID
            
        Returns:
            Photoshoot details or None
        """
        try:
            photoshoot = await mongo_service.find_one(
                "photoshoot_data",
                {"id": user_id, "photoshoot_id": photoshoot_id}
            )
            return photoshoot
        except Exception as e:
            logger.error(f"Error getting photoshoot: {str(e)}")
            raise
    
    async def list_photoshoots(
        self,
        user_id: str,
        filters: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        List user's photoshoots with filters
        
        Args:
            user_id: User ID
            filters: Optional filters
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of photoshoots
        """
        try:
            query = {"id": user_id}
            
            # Apply filters
            if filters:
                if filters.get("status"):
                    query["status"] = filters["status"]
                if filters.get("garment_type"):
                    query["upload_garment_type"] = filters["garment_type"]
                if filters.get("gender"):
                    query["gender"] = filters["gender"]
            
            photoshoots = await mongo_service.find_many(
                "photoshoot_data",
                query,
                skip=skip,
                limit=limit,
                sort=[("created_at", -1)]
            )
            
            return photoshoots
            
        except Exception as e:
            logger.error(f"Error listing photoshoots: {str(e)}")
            raise
    
    async def update_photoshoot_status(
        self,
        user_id: str,
        photoshoot_id: str,
        status: str,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Update photoshoot status
        
        Args:
            user_id: User ID
            photoshoot_id: Photoshoot ID
            status: New status
            additional_data: Additional data to update
            
        Returns:
            True if updated successfully
        """
        try:
            update_data = {"status": status}
            if additional_data:
                update_data.update(additional_data)
            
            result = await mongo_service.update_one(
                "photoshoot_data",
                {"id": user_id, "photoshoot_id": photoshoot_id},
                {"$set": update_data}
            )
            
            return result > 0
            
        except Exception as e:
            logger.error(f"Error updating photoshoot status: {str(e)}")
            raise
    
    def upscale_image(self, input_image: str, output_image: str) -> bool:
        """
        Upscale image using realesrgan
        
        Args:
            input_image: Input image path
            output_image: Output image path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            subprocess.run(
                [
                    "./realesrgan-ncnn-vulkan",
                    "-i", input_image,
                    "-o", output_image,
                    "-n", "realesrgan-x4plus"
                ],
                check=True
            )
            return True
        except Exception as e:
            logger.warning(f"Image upscaling failed: {str(e)}")
            return False
    
    async def get_photoshoot_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's photoshoot statistics
        
        Args:
            user_id: User ID
            
        Returns:
            Statistics dictionary
        """
        try:
            all_photoshoots = await mongo_service.find_many(
                "photoshoot_data",
                {"id": user_id}
            )
            
            total_photoshoots = len(all_photoshoots)
            completed = sum(1 for p in all_photoshoots if p.get("is_completed"))
            pending = sum(1 for p in all_photoshoots if not p.get("is_completed"))
            total_images = sum(len(p.get("all_images", [])) for p in all_photoshoots)
            
            return {
                "total_photoshoots": total_photoshoots,
                "completed_photoshoots": completed,
                "pending_photoshoots": pending,
                "total_images": total_images
            }
            
        except Exception as e:
            logger.error(f"Error getting photoshoot statistics: {str(e)}")
            raise


# Create singleton instance
photoshoot_service = PhotoshootService()

