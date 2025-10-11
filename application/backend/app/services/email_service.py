"""
Email service for sending emails with HTML templates
"""
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class EmailService:
    """Email service for sending emails"""
    
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.email_from = settings.EMAIL_FROM
        self.email_from_name = settings.EMAIL_FROM_NAME
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None
    ) -> bool:
        """
        Send HTML email
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_body: HTML email body
            from_email: Optional sender email (defaults to configured email)
            from_name: Optional sender name (defaults to configured name)
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["From"] = f"{from_name or self.email_from_name} <{from_email or self.email_from}>"
            message["To"] = to_email
            message["Subject"] = subject
            
            # Attach HTML body
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)
            
            # Send email
            await aiosmtplib.send(
                message,
                hostname=self.smtp_server,
                port=self.smtp_port,
                username=self.smtp_username,
                password=self.smtp_password,
                start_tls=True
            )
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def get_otp_verification_template(self, otp: int) -> str:
        """Get OTP verification email template"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verify Your Email - Stylic AI</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333333;
            background-color: #f8fafc;
        }}
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 30px;
            text-align: center;
            border-radius: 8px 8px 0 0;
        }}
        .logo {{
            max-width: 150px;
            height: auto;
            margin-bottom: 20px;
        }}
        .header-title {{
            color: #ffffff;
            font-size: 28px;
            font-weight: 700;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }}
        .content {{
            padding: 40px 30px;
            text-align: center;
        }}
        .greeting {{
            font-size: 20px;
            color: #2d3748;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        .message {{
            font-size: 16px;
            color: #4a5568;
            margin-bottom: 30px;
            line-height: 1.7;
        }}
        .otp-container {{
            background: linear-gradient(135deg, #f0fff4 0%, #dcfce7 100%);
            border: 2px solid #10b981;
            border-radius: 12px;
            padding: 30px;
            margin: 30px 0;
        }}
        .otp-label {{
            font-size: 14px;
            color: #059669;
            font-weight: 600;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .otp-code {{
            font-size: 36px;
            font-weight: 700;
            color: #059669;
            letter-spacing: 8px;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
        }}
        .otp-note {{
            font-size: 12px;
            color: #6b7280;
            margin-top: 10px;
        }}
        .security-note {{
            background-color: #fef3c7;
            border: 1px solid #f59e0b;
            border-radius: 8px;
            padding: 20px;
            margin-top: 30px;
            text-align: left;
        }}
        .security-text {{
            font-size: 14px;
            color: #92400e;
            line-height: 1.5;
        }}
        .footer {{
            background-color: #2d3748;
            color: #a0aec0;
            text-align: center;
            padding: 30px;
            font-size: 14px;
        }}
        .footer-links {{
            margin: 15px 0;
        }}
        .footer-link {{
            color: #81e6d9;
            text-decoration: none;
            margin: 0 15px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <img src="{settings.DOMAIN_URL}/static/external/logo.png" alt="Stylic AI Logo" class="logo">
            <h1 class="header-title">Email Verification</h1>
        </div>
        <div class="content">
            <div class="greeting">Almost there! 🎉</div>
            <div class="message">
                Welcome to Stylic AI! To complete your registration and secure your account, please verify your email address using the code below.
            </div>
            <div class="otp-container">
                <div class="otp-label">Your Verification Code</div>
                <div class="otp-code">{otp}</div>
                <div class="otp-note">Enter this code in the verification field</div>
            </div>
            <div class="security-note">
                <div class="security-text">
                    <strong>Important:</strong> This verification code will expire in 10 minutes. If you didn't create an account with Stylic AI, please ignore this email.
                </div>
            </div>
        </div>
        <div class="footer">
            <div>
                <strong>Stylic AI</strong><br>
                Making AI accessible for everyone
            </div>
            <div class="footer-links">
                <a href="https://stylic.ai/contact-us" class="footer-link">Support</a>
                <a href="https://stylic.ai/privacy-policy" class="footer-link">Privacy Policy</a>
                <a href="https://stylic.ai/terms-and-condition" class="footer-link">Terms of Service</a>
            </div>
            <div style="margin-top: 20px; font-size: 12px; color: #718096;">
                © 2025 Stylic AI. All rights reserved.
            </div>
        </div>
    </div>
</body>
</html>
        """

