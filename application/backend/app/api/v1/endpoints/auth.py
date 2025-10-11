"""
Authentication API endpoints
"""
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends, Request
from app.schemas.user import (
    UserRegister,
    UserLogin,
    TokenResponse,
    UserResponse,
    OTPVerification,
    ForgotPassword,
    ResetPassword,
    ChangePassword
)
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    validate_password_strength,
    validate_email_domain
)
from app.services.mongo_service import mongo_service
from app.services.email_service import email_service
from app.api.v1.dependencies.auth import get_current_active_user
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()

# Temporary storage for OTP (in production, use Redis or database with TTL)
otp_storage: Dict[str, Dict[str, Any]] = {}


@router.post("/register", response_model=dict, status_code=status.HTTP_200_OK)
async def register(user_data: UserRegister):
    """
    Register a new user
    
    - Validates email domain (no temporary emails)
    - Checks if email already exists
    - Generates OTP and sends verification email
    - Stores user data temporarily until OTP verification
    """
    try:
        # Validate email domain
        if not validate_email_domain(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not valid. Temporary email addresses are not allowed."
            )
        
        # Check if user already exists
        existing_user = await mongo_service.find_one(
            "login_mapping",
            {"email": user_data.email}
        )
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company already exists. Please login with your credentials."
            )
        
        # Validate password strength
        if not validate_password_strength(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long"
            )
        
        # Generate unique user ID
        user_id = str(uuid.uuid4())
        all_users = await mongo_service.find_many("login_mapping", {})
        all_ids = [u["id"] for u in all_users]
        
        while user_id in all_ids:
            user_id = str(uuid.uuid4())
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Generate OTP
        otp = random.randint(100000, 999999)
        
        # Prepare user data
        company_data = {
            "id": user_id,
            "first_name": user_data.first_name.lower(),
            "last_name": user_data.last_name.lower(),
            "company_name": user_data.company_name.lower() if user_data.company_name else "",
            "email": user_data.email,
            "password": hashed_password,
            "phone": user_data.phone or "",
            "is_privacy_accepted": user_data.is_privacy_accepted,
            "credit": settings.DEFAULT_SIGNUP_CREDITS,
            "plan": "",
            "role": "company",
            "is_active": False,  # Will be activated after OTP verification
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        login_mapping_data = {
            "id": user_id,
            "email": user_data.email,
            "password": hashed_password,
            "role": "company",
            "is_active": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Store OTP and user data temporarily
        otp_storage[user_data.email] = {
            "otp": otp,
            "company_data": company_data,
            "login_mapping_data": login_mapping_data,
            "expires_at": datetime.utcnow() + timedelta(minutes=10)
        }
        
        # Send OTP email
        otp_html = email_service.get_otp_verification_template(otp)
        await email_service.send_email(
            user_data.email,
            "Account OTP Verification: Stylic AI",
            otp_html
        )
        
        logger.info(f"Registration initiated for {user_data.email}")
        
        return {
            "success": True,
            "message": "OTP sent successfully. Please check your email.",
            "email": user_data.email
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.post("/verify-otp", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def verify_otp(email: str, otp_data: OTPVerification):
    """
    Verify OTP and complete registration
    
    - Verifies OTP
    - Creates user account
    - Sends welcome email
    - Returns authentication tokens
    """
    try:
        # Check if OTP exists
        if email not in otp_storage:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP not found or expired. Please register again."
            )
        
        stored_data = otp_storage[email]
        
        # Check if OTP expired
        if datetime.utcnow() > stored_data["expires_at"]:
            del otp_storage[email]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP expired. Please register again."
            )
        
        # Verify OTP
        if otp_data.otp != stored_data["otp"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP. Please try again."
            )
        
        # Create user account
        company_data = stored_data["company_data"]
        login_mapping_data = stored_data["login_mapping_data"]
        
        # Activate account
        company_data["is_active"] = True
        login_mapping_data["is_active"] = True
        
        # Insert into database
        await mongo_service.insert_one("company_data", company_data)
        await mongo_service.insert_one("login_mapping", login_mapping_data)
        
        # Remove from temporary storage
        del otp_storage[email]
        
        # Send welcome email
        welcome_html = email_service.get_welcome_email_template(company_data["first_name"])
        await email_service.send_email(
            email,
            f"Welcome {company_data['first_name']}",
            welcome_html
        )
        
        # Generate tokens
        access_token = create_access_token({"sub": company_data["id"]})
        refresh_token = create_refresh_token({"sub": company_data["id"]})
        
        # Prepare user response
        user_response = UserResponse(
            id=company_data["id"],
            email=company_data["email"],
            first_name=company_data["first_name"],
            last_name=company_data["last_name"],
            company_name=company_data.get("company_name", ""),
            phone=company_data.get("phone", ""),
            credit=company_data["credit"],
            plan=company_data["plan"],
            role=company_data["role"],
            is_active=company_data["is_active"],
            created_at=company_data["created_at"],
            updated_at=company_data["updated_at"]
        )
        
        logger.info(f"User registered successfully: {email}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in OTP verification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during OTP verification"
        )

