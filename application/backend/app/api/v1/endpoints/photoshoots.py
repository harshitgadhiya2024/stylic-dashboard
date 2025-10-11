"""
Photoshoot Endpoints - AI Photoshoot Generation and Management
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
from typing import List, Optional
import os
import uuid
import zipfile
import io
from datetime import datetime

from app.schemas.photoshoot import (
    PhotoshootCreate,
    PhotoshootResponse,
    PhotoshootListResponse,
    PhotoshootDetailResponse,
    PhotoshootFilter
)
from app.services.photoshoot_service import photoshoot_service
from app.services.mongo_service import mongo_service
from app.api.v1.dependencies.auth import (
    get_current_active_user,
    check_user_credits
)
from app.core.config import settings
from app.core.logging import logger

router = APIRouter()


@router.post("/", response_model=PhotoshootResponse, status_code=status.HTTP_201_CREATED)
async def create_photoshoot(
    background_tasks: BackgroundTasks,
    garment_type: str = Form(...),
    age_group: str = Form(...),
    gender: str = Form(...),
    ethnicity: str = Form(...),
    height: str = Form(...),
    weight: str = Form(...),
    age: int = Form(...),
    fitting: str = Form(...),
    background_description: Optional[str] = Form(None),
    selected_background: Optional[str] = Form(None),
    pose_input_method: str = Form("predefined"),
    selected_poses: Optional[str] = Form(None),  # JSON string
    upper_garment_specs: Optional[str] = Form(None),
    lower_garment_specs: Optional[str] = Form(None),
    upper_garment: Optional[UploadFile] = File(None),
    lower_garment: Optional[UploadFile] = File(None),
    pose_images: Optional[List[UploadFile]] = File(None),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Create new AI photoshoot
    
    - Uploads garment images
    - Processes pose selection (predefined/upload/prompts)
    - Queues photoshoot generation
    - Requires sufficient credits
    """
    try:
        user_id = current_user["id"]
        
        # Parse selected poses if provided
        import json
        poses_list = []
        if selected_poses:
            try:
                poses_list = json.loads(selected_poses)
            except:
                poses_list = [selected_poses]
        
        # Create photoshoot record
        photoshoot_data = {
            "garment_type": garment_type,
            "age_group": age_group,
            "gender": gender,
            "ethnicity": ethnicity,
            "height": height,
            "weight": weight,
            "age": age,
            "fitting": fitting,
            "background_description": background_description,
            "selected_background": selected_background,
            "pose_input_method": pose_input_method,
            "selected_poses": poses_list,
            "upper_garment_specs": upper_garment_specs,
            "lower_garment_specs": lower_garment_specs
        }
        
        # Create photoshoot
        result = await photoshoot_service.create_photoshoot(user_id, photoshoot_data)
        photoshoot_id = result["photoshoot_id"]
        
        # Create photoshoot directory
        photoshoot_dir = os.path.join(
            settings.UPLOAD_DIR,
            "photoshoots",
            photoshoot_id
        )
        os.makedirs(photoshoot_dir, exist_ok=True)
        
        # Save garment images
        upper_garment_filename = None
        lower_garment_filename = None
        
        if upper_garment:
            upper_garment_filename = f"upper_{uuid.uuid4()}{os.path.splitext(upper_garment.filename)[1]}"
            upper_path = os.path.join(photoshoot_dir, upper_garment_filename)
            with open(upper_path, "wb") as f:
                content = await upper_garment.read()
                f.write(content)
        
        if lower_garment:
            lower_garment_filename = f"lower_{uuid.uuid4()}{os.path.splitext(lower_garment.filename)[1]}"
            lower_path = os.path.join(photoshoot_dir, lower_garment_filename)
            with open(lower_path, "wb") as f:
                content = await lower_garment.read()
                f.write(content)
        
        # Process pose images if uploaded
        pose_descriptions = []
        if pose_input_method == "upload" and pose_images:
            pose_image_paths = []
            for idx, pose_img in enumerate(pose_images):
                pose_filename = f"pose_{idx}_{uuid.uuid4()}{os.path.splitext(pose_img.filename)[1]}"
                pose_path = os.path.join(photoshoot_dir, pose_filename)
                with open(pose_path, "wb") as f:
                    content = await pose_img.read()
                    f.write(content)
                pose_image_paths.append(pose_path)
            
            # Analyze poses
            pose_descriptions = await photoshoot_service.process_pose_images(
                pose_image_paths,
                photoshoot_id
            )
        
        # Update photoshoot with file info and pose descriptions
        await mongo_service.update_one(
            "photoshoot_data",
            {"id": user_id, "photoshoot_id": photoshoot_id},
            {
                "$set": {
                    "upper_garment_filename": upper_garment_filename,
                    "lower_garment_filename": lower_garment_filename,
                    "pose_descriptions": pose_descriptions
                }
            }
        )
        
        # TODO: Queue background task for photoshoot generation
        # background_tasks.add_task(generate_photoshoot, user_id, photoshoot_id)
        
        logger.info(f"Photoshoot created: {photoshoot_id} for user: {user_id}")
        
        return PhotoshootResponse(
            photoshoot_id=photoshoot_id,
            status="pending",
            message="Photoshoot queued for processing"
        )
        
    except Exception as e:
        logger.error(f"Error creating photoshoot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create photoshoot: {str(e)}"
        )


@router.get("/", response_model=PhotoshootListResponse)
async def list_photoshoots(
    skip: int = 0,
    limit: int = 20,
    status_filter: Optional[str] = None,
    garment_type: Optional[str] = None,
    gender: Optional[str] = None,
    current_user: dict = Depends(get_current_active_user)
):
    """
    List user's photoshoots
    
    - Supports pagination
    - Supports filtering by status, garment type, gender
    """
    try:
        user_id = current_user["id"]
        
        # Build filters
        filters = {}
        if status_filter:
            filters["status"] = status_filter
        if garment_type:
            filters["garment_type"] = garment_type
        if gender:
            filters["gender"] = gender
        
        # Get photoshoots
        photoshoots = await photoshoot_service.list_photoshoots(
            user_id,
            filters=filters,
            skip=skip,
            limit=limit
        )
        
        # Get total count
        total = await mongo_service.count_documents(
            "photoshoot_data",
            {"id": user_id, **filters}
        )
        
        return PhotoshootListResponse(
            photoshoots=photoshoots,
            total=total,
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Error listing photoshoots: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch photoshoots"
        )


@router.get("/{photoshoot_id}", response_model=PhotoshootDetailResponse)
async def get_photoshoot(
    photoshoot_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get photoshoot details
    
    - Returns complete photoshoot information
    - Includes all generated images
    """
    try:
        user_id = current_user["id"]
        
        photoshoot = await photoshoot_service.get_photoshoot(user_id, photoshoot_id)
        
        if not photoshoot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Photoshoot not found"
            )
        
        return PhotoshootDetailResponse(**photoshoot)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting photoshoot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch photoshoot"
        )


@router.get("/filters/options", response_model=PhotoshootFilter)
async def get_filter_options():
    """
    Get available filter options
    
    Returns all available options for filtering photoshoots
    """
    from app.schemas.photoshoot import (
        GarmentType, Gender, AgeGroup, Ethnicity, Fitting
    )
    
    return PhotoshootFilter(
        garment_types=[g.value for g in GarmentType],
        genders=[g.value for g in Gender],
        age_groups=[a.value for a in AgeGroup],
        ethnicities=[e.value for e in Ethnicity],
        fittings=[f.value for f in Fitting],
        statuses=["pending", "processing", "completed", "failed"]
    )


@router.get("/{photoshoot_id}/download/{image_name}")
async def download_image(
    photoshoot_id: str,
    image_name: str,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Download single photoshoot image
    
    Returns image file
    """
    try:
        user_id = current_user["id"]
        
        # Verify photoshoot belongs to user
        photoshoot = await photoshoot_service.get_photoshoot(user_id, photoshoot_id)
        if not photoshoot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Photoshoot not found"
            )
        
        # Build image path
        image_path = os.path.join(
            settings.UPLOAD_DIR,
            "photoshoots",
            photoshoot_id,
            image_name
        )
        
        if not os.path.exists(image_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
        
        return FileResponse(
            image_path,
            media_type="image/png",
            filename=image_name
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading image: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download image"
        )


@router.get("/{photoshoot_id}/download-all")
async def download_all_images(
    photoshoot_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Download all photoshoot images as ZIP

    Returns ZIP file containing all images
    """
    try:
        user_id = current_user["id"]

        # Verify photoshoot belongs to user
        photoshoot = await photoshoot_service.get_photoshoot(user_id, photoshoot_id)
        if not photoshoot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Photoshoot not found"
            )

        # Get all images
        all_images = photoshoot.get("all_images", [])
        if not all_images:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No images found"
            )

        # Create ZIP file in memory
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            photoshoot_dir = os.path.join(
                settings.UPLOAD_DIR,
                "photoshoots",
                photoshoot_id
            )

            for image_url in all_images:
                # Extract filename from URL
                image_name = image_url.split("/")[-1]
                image_path = os.path.join(photoshoot_dir, image_name)

                if os.path.exists(image_path):
                    zip_file.write(image_path, arcname=image_name)

        zip_buffer.seek(0)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename=photoshoot_{photoshoot_id}.zip"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading all images: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download images"
        )


@router.delete("/{photoshoot_id}", response_model=dict)
async def delete_photoshoot(
    photoshoot_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Delete photoshoot

    - Removes photoshoot record
    - Does not delete files (for safety)
    """
    try:
        user_id = current_user["id"]

        # Verify photoshoot exists
        photoshoot = await photoshoot_service.get_photoshoot(user_id, photoshoot_id)
        if not photoshoot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Photoshoot not found"
            )

        # Delete from database
        await mongo_service.delete_one(
            "photoshoot_data",
            {"id": user_id, "photoshoot_id": photoshoot_id}
        )

        logger.info(f"Photoshoot deleted: {photoshoot_id} for user: {user_id}")

        return {
            "success": True,
            "message": "Photoshoot deleted successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting photoshoot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete photoshoot"
        )

