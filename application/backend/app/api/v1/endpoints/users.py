"""
User Management Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from app.schemas.user import UserResponse, UpdateProfile
from app.services.mongo_service import mongo_service
from app.api.v1.dependencies.auth import (
    get_current_active_user,
    get_current_user_with_credits
)
from app.core.logging import logger

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user_with_credits)
):
    """
    Get current user profile
    
    Returns complete user information including credits
    """
    try:
        return UserResponse(**current_user)
    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user profile"
        )


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    profile_data: UpdateProfile,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Update user profile
    
    - Updates user information
    - Returns updated profile
    """
    try:
        user_id = current_user["id"]
        email = current_user["email"]
        
        # Prepare update data
        update_data = {}
        if profile_data.first_name is not None:
            update_data["first_name"] = profile_data.first_name.lower()
        if profile_data.last_name is not None:
            update_data["last_name"] = profile_data.last_name.lower()
        if profile_data.company_name is not None:
            update_data["company_name"] = profile_data.company_name.lower()
        if profile_data.phone is not None:
            update_data["phone"] = profile_data.phone
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update"
            )
        
        # Update in both collections
        await mongo_service.update_one(
            "company_data",
            {"id": user_id},
            {"$set": update_data}
        )
        
        await mongo_service.update_one(
            "login_mapping",
            {"email": email},
            {"$set": update_data}
        )
        
        # Get updated user data
        updated_user = await mongo_service.find_one(
            "company_data",
            {"id": user_id}
        )
        
        logger.info(f"Profile updated for user: {email}")
        
        return UserResponse(**updated_user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )


@router.get("/me/credits", response_model=dict)
async def get_user_credits(
    current_user: dict = Depends(get_current_user_with_credits)
):
    """
    Get user's current credit balance
    
    Returns credit information
    """
    try:
        return {
            "credits": current_user.get("credit", 0),
            "plan": current_user.get("plan", ""),
            "user_id": current_user["id"]
        }
    except Exception as e:
        logger.error(f"Error getting user credits: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch credits"
        )


@router.get("/me/statistics", response_model=dict)
async def get_user_statistics(
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get user's statistics
    
    Returns photoshoot and order statistics
    """
    try:
        user_id = current_user["id"]
        
        # Get photoshoot statistics
        photoshoots = await mongo_service.find_many(
            "photoshoot_data",
            {"id": user_id}
        )
        
        total_photoshoots = len(photoshoots)
        completed_photoshoots = sum(
            1 for p in photoshoots if p.get("is_completed", False)
        )
        pending_photoshoots = sum(
            1 for p in photoshoots if not p.get("is_completed", False)
        )
        total_images = sum(
            len(p.get("all_images", [])) for p in photoshoots
        )
        
        # Get order statistics
        orders = await mongo_service.find_many(
            "order_data",
            {"id": user_id}
        )
        
        total_orders = len(orders)
        successful_orders = sum(
            1 for o in orders if o.get("status") == "success"
        )
        total_spent = sum(
            o.get("amount", 0) for o in orders if o.get("status") == "success"
        )
        
        return {
            "photoshoots": {
                "total": total_photoshoots,
                "completed": completed_photoshoots,
                "pending": pending_photoshoots,
                "total_images": total_images
            },
            "orders": {
                "total": total_orders,
                "successful": successful_orders,
                "total_spent": total_spent
            },
            "credits": {
                "current": current_user.get("credit", 0),
                "plan": current_user.get("plan", "")
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting user statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch statistics"
        )


@router.delete("/me", response_model=dict)
async def delete_user_account(
    current_user: dict = Depends(get_current_active_user)
):
    """
    Delete user account (soft delete)
    
    - Deactivates user account
    - Does not delete data
    """
    try:
        user_id = current_user["id"]
        email = current_user["email"]
        
        # Soft delete - just deactivate the account
        await mongo_service.update_one(
            "company_data",
            {"id": user_id},
            {"$set": {"is_active": False}}
        )
        
        await mongo_service.update_one(
            "login_mapping",
            {"email": email},
            {"$set": {"is_active": False}}
        )
        
        logger.info(f"Account deactivated for user: {email}")
        
        return {
            "success": True,
            "message": "Account deactivated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error deleting account: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete account"
        )

