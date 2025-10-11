"""
Payment-related Pydantic schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class CreateOrderRequest(BaseModel):
    """Create order request schema"""
    amount: int = Field(..., gt=0)
    credit: int = Field(..., gt=0)
    currency: str = "INR"
    coupon_code: Optional[str] = None


class CreateOrderResponse(BaseModel):
    """Create order response schema"""
    success: bool = True
    order_id: str
    amount: int
    currency: str = "INR"
    key_id: str
    discount: int = 0


class VerifyPaymentRequest(BaseModel):
    """Verify payment request schema"""
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str


class CouponValidation(BaseModel):
    """Coupon validation schema"""
    code: str = Field(..., min_length=1)


class CouponResponse(BaseModel):
    """Coupon response schema"""
    valid: bool
    discount: int = 0


class OrderResponse(BaseModel):
    """Order response schema"""
    id: str
    order_id: str
    payment_id: str
    credit: int
    amount: int
    currency: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderHistoryResponse(BaseModel):
    """Order history response schema"""
    success: bool = True
    data: list[OrderResponse]
    total: int


class CreditHistoryItem(BaseModel):
    """Credit history item schema"""
    type: str  # "purchase", "debit", "refund"
    amount: int
    description: str
    created_at: datetime


class CreditHistoryResponse(BaseModel):
    """Credit history response schema"""
    transaction_id: str
    type: str  # "credit" or "debit"
    amount: int
    description: str
    payment_amount: int = 0
    status: str = "completed"
    created_at: datetime

    class Config:
        from_attributes = True


class CreditPackage(BaseModel):
    """Credit package schema"""
    id: str
    name: str
    credits: int
    amount: int
    description: str
    popular: bool = False

