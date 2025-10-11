"""
Authentication dependencies for FastAPI routes
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token
from app.services.mongo_service import mongo_service
from app.core.logging import get_logger

logger = get_logger(__name__)

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Bearer credentials
        
    Returns:
        User document from database
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        # Decode token
        token = credentials.credentials
        payload = decode_token(token)
        
        # Get user ID from token
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        user = await mongo_service.find_one(
            "company_data",
            {"id": user_id}
        )
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.get("is_active", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Get current active user
    
    Args:
        current_user: Current user from get_current_user dependency
        
    Returns:
        Active user document
        
    Raises:
        HTTPException: If user is not active
    """
    if not current_user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def get_current_user_with_credits(
    current_user: dict = Depends(get_current_active_user)
) -> dict:
    """
    Get current user with updated credit information
    
    Args:
        current_user: Current active user
        
    Returns:
        User document with current credit balance
    """
    # Refresh credit information from database
    user = await mongo_service.find_one(
        "company_data",
        {"id": current_user["id"]}
    )
    
    if user:
        current_user["credit"] = user.get("credit", 0)
    
    return current_user


def check_user_credits(required_credits: int):
    """
    Dependency factory to check if user has sufficient credits
    
    Args:
        required_credits: Number of credits required
        
    Returns:
        Dependency function
    """
    async def _check_credits(
        current_user: dict = Depends(get_current_user_with_credits)
    ) -> dict:
        """Check if user has sufficient credits"""
        user_credits = current_user.get("credit", 0)
        
        if user_credits < required_credits:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=f"Insufficient credits. Required: {required_credits}, Available: {user_credits}"
            )
        
        return current_user
    
    return _check_credits


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[dict]:
    """
    Get current user if authenticated, otherwise return None
    
    Args:
        credentials: Optional HTTP Bearer credentials
        
    Returns:
        User document or None
    """
    if credentials is None:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None

