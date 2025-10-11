"""
Payment Service - Razorpay Integration
"""
import razorpay
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger


class PaymentService:
    """Service for handling Razorpay payment operations"""
    
    def __init__(self):
        """Initialize Razorpay client"""
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        # Set app details
        self.client.set_app_details({
            "title": "Stylic AI",
            "version": "1.0.0"
        })
        
        # Coupon codes and their credit values
        self.coupons = {
            "WELCOME10": {"credit": 10, "discount_percent": 10},
            "SAVE20": {"credit": 20, "discount_percent": 20},
            "MEGA50": {"credit": 50, "discount_percent": 25},
        }
    
    def create_order(
        self,
        amount: int,
        currency: str = "INR",
        notes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a Razorpay order
        
        Args:
            amount: Amount in rupees (will be converted to paisa)
            currency: Currency code (default: INR)
            notes: Additional notes for the order
            
        Returns:
            Order details from Razorpay
        """
        try:
            # Convert amount to paisa
            amount_paisa = int(amount * 100)
            
            order_data = {
                'amount': amount_paisa,
                'currency': currency,
                'payment_capture': 1,  # Auto capture payment
                'notes': notes or {
                    'created_by': 'Stylic AI',
                    'version': '1.0.0'
                }
            }
            
            order = self.client.order.create(data=order_data)
            logger.info(f"Razorpay order created: {order['id']}")
            
            return {
                'order_id': order['id'],
                'amount': order['amount'],
                'currency': order['currency'],
                'status': order['status']
            }
            
        except razorpay.errors.BadRequestError as e:
            logger.error(f"Razorpay bad request error: {str(e)}")
            raise ValueError(f"Bad request: {str(e)}")
        except razorpay.errors.ServerError as e:
            logger.error(f"Razorpay server error: {str(e)}")
            raise Exception(f"Server error: {str(e)}")
        except Exception as e:
            logger.error(f"Error creating Razorpay order: {str(e)}")
            raise
    
    def verify_payment_signature(
        self,
        order_id: str,
        payment_id: str,
        signature: str
    ) -> bool:
        """
        Verify Razorpay payment signature
        
        Args:
            order_id: Razorpay order ID
            payment_id: Razorpay payment ID
            signature: Payment signature
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            self.client.utility.verify_payment_signature(params_dict)
            logger.info(f"Payment signature verified: {payment_id}")
            return True
            
        except razorpay.errors.SignatureVerificationError:
            logger.warning(f"Payment signature verification failed: {payment_id}")
            return False
        except Exception as e:
            logger.error(f"Error verifying payment signature: {str(e)}")
            return False
    
    def fetch_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Fetch payment details from Razorpay
        
        Args:
            payment_id: Razorpay payment ID
            
        Returns:
            Payment details
        """
        try:
            payment = self.client.payment.fetch(payment_id)
            return payment
        except Exception as e:
            logger.error(f"Error fetching payment: {str(e)}")
            raise
    
    def fetch_order(self, order_id: str) -> Dict[str, Any]:
        """
        Fetch order details from Razorpay
        
        Args:
            order_id: Razorpay order ID
            
        Returns:
            Order details
        """
        try:
            order = self.client.order.fetch(order_id)
            return order
        except Exception as e:
            logger.error(f"Error fetching order: {str(e)}")
            raise
    
    def validate_coupon(self, coupon_code: str) -> Optional[Dict[str, Any]]:
        """
        Validate coupon code
        
        Args:
            coupon_code: Coupon code to validate
            
        Returns:
            Coupon details if valid, None otherwise
        """
        coupon = self.coupons.get(coupon_code.upper())
        if coupon:
            logger.info(f"Valid coupon applied: {coupon_code}")
            return coupon
        logger.warning(f"Invalid coupon code: {coupon_code}")
        return None
    
    def calculate_discounted_amount(
        self,
        amount: int,
        coupon_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate discounted amount with coupon
        
        Args:
            amount: Original amount
            coupon_code: Optional coupon code
            
        Returns:
            Dictionary with original amount, discount, and final amount
        """
        discount = 0
        discount_percent = 0
        
        if coupon_code:
            coupon = self.validate_coupon(coupon_code)
            if coupon:
                discount_percent = coupon.get('discount_percent', 0)
                discount = int(amount * discount_percent / 100)
        
        final_amount = amount - discount
        
        return {
            'original_amount': amount,
            'discount': discount,
            'discount_percent': discount_percent,
            'final_amount': final_amount
        }
    
    def get_credit_packages(self) -> list:
        """
        Get available credit packages
        
        Returns:
            List of credit packages
        """
        return [
            {
                "id": "starter",
                "name": "Starter Pack",
                "credits": 10,
                "amount": 99,
                "description": "Perfect for trying out our service",
                "popular": False
            },
            {
                "id": "basic",
                "name": "Basic Pack",
                "credits": 25,
                "amount": 199,
                "description": "Great for small projects",
                "popular": False
            },
            {
                "id": "pro",
                "name": "Pro Pack",
                "credits": 50,
                "amount": 349,
                "description": "Most popular choice",
                "popular": True
            },
            {
                "id": "business",
                "name": "Business Pack",
                "credits": 100,
                "amount": 599,
                "description": "For professional use",
                "popular": False
            },
            {
                "id": "enterprise",
                "name": "Enterprise Pack",
                "credits": 250,
                "amount": 1299,
                "description": "For large scale operations",
                "popular": False
            }
        ]


# Create singleton instance
payment_service = PaymentService()

