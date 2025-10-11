"""
Payment Endpoints - Razorpay Integration
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from datetime import datetime
import uuid

from app.schemas.payment import (
    CreateOrderRequest,
    CreateOrderResponse,
    VerifyPaymentRequest,
    CouponValidation,
    OrderResponse,
    CreditPackage
)
from app.services.payment_service import payment_service
from app.services.mongo_service import mongo_service
from app.api.v1.dependencies.auth import get_current_active_user
from app.core.config import settings
from app.core.logging import logger

router = APIRouter()


@router.get("/packages", response_model=list[CreditPackage])
async def get_credit_packages():
    """
    Get available credit packages
    
    Returns list of credit packages with pricing
    """
    try:
        packages = payment_service.get_credit_packages()
        return packages
    except Exception as e:
        logger.error(f"Error getting credit packages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch credit packages"
        )


@router.post("/create-order", response_model=CreateOrderResponse)
async def create_order(
    request: CreateOrderRequest,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Create Razorpay order for credit purchase
    
    - Creates order in Razorpay
    - Stores order details in database
    - Returns order ID and payment details
    """
    try:
        user_id = current_user["id"]
        
        # Calculate final amount with coupon if provided
        amount_details = payment_service.calculate_discounted_amount(
            request.amount,
            request.coupon_code
        )
        
        final_amount = amount_details['final_amount']
        
        # Create Razorpay order
        order = payment_service.create_order(
            amount=final_amount,
            currency=request.currency,
            notes={
                "user_id": user_id,
                "credits": request.credit,
                "coupon_code": request.coupon_code or ""
            }
        )
        
        # Store order details in database (pending status)
        order_record = {
            "id": user_id,
            "order_id": order['order_id'],
            "payment_id": "",
            "credit": request.credit,
            "amount": final_amount,
            "original_amount": request.amount,
            "discount": amount_details['discount'],
            "coupon_code": request.coupon_code or "",
            "currency": request.currency,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await mongo_service.insert_one("order_data", order_record)
        
        logger.info(f"Order created for user {user_id}: {order['order_id']}")
        
        return CreateOrderResponse(
            success=True,
            order_id=order['order_id'],
            amount=order['amount'],
            currency=order['currency'],
            key_id=settings.RAZORPAY_KEY_ID,
            discount=amount_details['discount']
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
        )


@router.post("/verify", response_model=dict)
async def verify_payment(
    request: VerifyPaymentRequest,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Verify Razorpay payment signature
    
    - Verifies payment signature
    - Updates order status
    - Credits user account
    """
    try:
        user_id = current_user["id"]
        
        # Verify payment signature
        is_valid = payment_service.verify_payment_signature(
            request.razorpay_order_id,
            request.razorpay_payment_id,
            request.razorpay_signature
        )
        
        if not is_valid:
            # Update order as failed
            await mongo_service.update_one(
                "order_data",
                {"id": user_id, "order_id": request.razorpay_order_id},
                {
                    "$set": {
                        "payment_id": request.razorpay_payment_id,
                        "status": "failed",
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment verification failed"
            )
        
        # Get order details
        order = await mongo_service.find_one(
            "order_data",
            {"id": user_id, "order_id": request.razorpay_order_id}
        )
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Update order as successful
        await mongo_service.update_one(
            "order_data",
            {"id": user_id, "order_id": request.razorpay_order_id},
            {
                "$set": {
                    "payment_id": request.razorpay_payment_id,
                    "status": "success",
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Credit user account
        user = await mongo_service.find_one(
            "company_data",
            {"id": user_id}
        )
        
        current_credits = int(user.get("credit", 0))
        new_credits = current_credits + int(order["credit"])
        
        await mongo_service.update_one(
            "company_data",
            {"id": user_id},
            {"$set": {"credit": new_credits}}
        )
        
        logger.info(f"Payment verified for user {user_id}: {request.razorpay_payment_id}")
        
        return {
            "success": True,
            "message": "Payment verified successfully",
            "credits_added": order["credit"],
            "total_credits": new_credits
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying payment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify payment"
        )


@router.get("/validate-coupon", response_model=dict)
async def validate_coupon(
    coupon_code: str,
    amount: int,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Validate coupon code
    
    - Checks if coupon is valid
    - Returns discount details
    """
    try:
        coupon = payment_service.validate_coupon(coupon_code)
        
        if not coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid coupon code"
            )
        
        # Calculate discount
        amount_details = payment_service.calculate_discounted_amount(
            amount,
            coupon_code
        )
        
        return {
            "success": True,
            "valid": True,
            "coupon_code": coupon_code.upper(),
            "discount_percent": amount_details['discount_percent'],
            "discount": amount_details['discount'],
            "original_amount": amount_details['original_amount'],
            "final_amount": amount_details['final_amount']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating coupon: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to validate coupon"
        )


@router.get("/orders", response_model=list[OrderResponse])
async def get_orders(
    skip: int = 0,
    limit: int = 20,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get user's order history
    
    - Returns list of orders
    - Supports pagination
    """
    try:
        user_id = current_user["id"]
        
        orders = await mongo_service.find_many(
            "order_data",
            {"id": user_id},
            skip=skip,
            limit=limit,
            sort=[("created_at", -1)]
        )
        
        return orders
        
    except Exception as e:
        logger.error(f"Error getting orders: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch orders"
        )


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get specific order details
    
    - Returns order information
    """
    try:
        user_id = current_user["id"]
        
        order = await mongo_service.find_one(
            "order_data",
            {"id": user_id, "order_id": order_id}
        )
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        return order
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch order"
        )

