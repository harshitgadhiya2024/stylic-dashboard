"""
Credit Management Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime

from app.schemas.payment import CreditHistoryResponse
from app.services.mongo_service import mongo_service
from app.api.v1.dependencies.auth import get_current_active_user
from app.core.logging import logger

router = APIRouter()


@router.get("/balance", response_model=dict)
async def get_credit_balance(
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get current credit balance
    
    Returns user's current credit balance
    """
    try:
        user_id = current_user["id"]
        
        # Get fresh user data
        user = await mongo_service.find_one(
            "company_data",
            {"id": user_id}
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "credits": user.get("credit", 0),
            "plan": user.get("plan", ""),
            "user_id": user_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting credit balance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch credit balance"
        )


@router.get("/history", response_model=List[CreditHistoryResponse])
async def get_credit_history(
    skip: int = 0,
    limit: int = 50,
    transaction_type: Optional[str] = None,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get credit transaction history
    
    - Returns list of credit transactions
    - Supports pagination
    - Can filter by transaction type (credit/debit)
    """
    try:
        user_id = current_user["id"]
        
        # Get orders (credit transactions)
        order_query = {"id": user_id}
        if transaction_type == "credit":
            order_query["status"] = "success"
        
        orders = await mongo_service.find_many(
            "order_data",
            order_query,
            skip=0 if transaction_type == "debit" else skip,
            limit=limit if transaction_type != "debit" else 0,
            sort=[("created_at", -1)]
        )
        
        # Get photoshoots (debit transactions)
        photoshoot_query = {"id": user_id, "is_credit_debited": True}
        
        photoshoots = await mongo_service.find_many(
            "photoshoot_data",
            photoshoot_query,
            skip=0 if transaction_type == "credit" else skip,
            limit=limit if transaction_type != "credit" else 0,
            sort=[("created_at", -1)]
        )
        
        # Combine and format transactions
        transactions = []
        
        # Add credit transactions from orders
        if transaction_type != "debit":
            for order in orders:
                if order.get("status") == "success":
                    transactions.append({
                        "transaction_id": order.get("order_id", ""),
                        "type": "credit",
                        "amount": order.get("credit", 0),
                        "description": f"Credit purchase - {order.get('credit', 0)} credits",
                        "payment_amount": order.get("amount", 0),
                        "created_at": order.get("created_at"),
                        "status": "completed"
                    })
        
        # Add debit transactions from photoshoots
        if transaction_type != "credit":
            for photoshoot in photoshoots:
                transactions.append({
                    "transaction_id": photoshoot.get("photoshoot_id", ""),
                    "type": "debit",
                    "amount": photoshoot.get("total_credit", 0),
                    "description": f"Photoshoot generation - {len(photoshoot.get('all_images', []))} images",
                    "payment_amount": 0,
                    "created_at": photoshoot.get("created_at"),
                    "status": "completed" if photoshoot.get("is_completed") else "pending"
                })
        
        # Sort by date
        transactions.sort(key=lambda x: x.get("created_at", datetime.min), reverse=True)
        
        # Apply pagination if both types
        if not transaction_type:
            transactions = transactions[skip:skip + limit]
        
        return transactions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting credit history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch credit history"
        )


@router.get("/statistics", response_model=dict)
async def get_credit_statistics(
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get credit usage statistics
    
    Returns detailed credit statistics
    """
    try:
        user_id = current_user["id"]
        
        # Get all successful orders
        orders = await mongo_service.find_many(
            "order_data",
            {"id": user_id, "status": "success"}
        )
        
        total_purchased = sum(order.get("credit", 0) for order in orders)
        total_spent = sum(order.get("amount", 0) for order in orders)
        
        # Get all completed photoshoots
        photoshoots = await mongo_service.find_many(
            "photoshoot_data",
            {"id": user_id, "is_credit_debited": True}
        )
        
        total_used = sum(ps.get("total_credit", 0) for ps in photoshoots)
        total_images = sum(len(ps.get("all_images", [])) for ps in photoshoots)
        
        # Get current balance
        user = await mongo_service.find_one(
            "company_data",
            {"id": user_id}
        )
        
        current_balance = user.get("credit", 0)
        
        return {
            "current_balance": current_balance,
            "total_purchased": total_purchased,
            "total_used": total_used,
            "total_spent": total_spent,
            "total_images_generated": total_images,
            "total_photoshoots": len(photoshoots),
            "total_orders": len(orders),
            "average_cost_per_image": round(total_spent / total_images, 2) if total_images > 0 else 0
        }
        
    except Exception as e:
        logger.error(f"Error getting credit statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch credit statistics"
        )


@router.post("/transfer", response_model=dict)
async def transfer_credits(
    to_user_email: str,
    amount: int,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Transfer credits to another user (Admin feature - disabled for now)
    
    - Transfers credits from one user to another
    - Requires admin privileges
    """
    # This is a placeholder for future admin functionality
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Credit transfer feature is not yet implemented"
    )

