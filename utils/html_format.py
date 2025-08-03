from datetime import datetime
from flask import session


class htmlOperation():

    def __init__(self):
        pass

    def otp_verification_process(self, otp):
        try:
            otp_verification = f"""
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
                        
                        .security-icon {{
                            color: #d97706;
                            font-size: 20px;
                            margin-right: 8px;
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
                        
                        .footer-link:hover {{
                            color: #ffffff;
                        }}
                        
                        @media only screen and (max-width: 600px) {{
                            .email-container {{
                                margin: 0;
                                border-radius: 0;
                            }}
                            
                            .header, .content, .footer {{
                                padding: 25px 20px;
                            }}
                            
                            .header-title {{
                                font-size: 24px;
                            }}
                            
                            .otp-code {{
                                font-size: 28px;
                                letter-spacing: 4px;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <img src="https://app.stylic.ai/static/external/logo.png" alt="Stylic AI Logo" class="logo">
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
                                <div style="display: flex; align-items: flex-start;">
                                    <span class="security-icon">⏰</span>
                                    <div class="security-text">
                                        <strong>Important:</strong> This verification code will expire in 10 minutes. If you didn't create an account with Stylic AI, please ignore this email.
                                    </div>
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

            return otp_verification

        except Exception as e:
            print(f"{datetime.now()}: Error in getting otp verification html format: {str(e)}")

    def photoshoot_faileur(self, photoshoot_id):
        try:
            photoshoot_faileur = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Stylic AI</title>
                    <style>
                        body {
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f5f5f5;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #f2f2f2;
                            box-shadow: 1px 1px 5px #2c3e50;
                        }
                        .header {
                            text-align: center;
                            padding: 20px 0;
                            border-bottom: 1px solid #eeeeee;
                        }
                        .logo {
                            font-size: 32px;
                            font-weight: bold;
                            color: #2c3e50;
                        }
                        .logo span {
                            color: #e74c3c;
                        }
                        .content {
                            padding: 30px 20px;
                            color: #333333;
                        }
                        .otp-container {
                            margin: 30px 0;
                            text-align: center;
                        }
                        .otp-code {
                            font-size: 32px;
                            font-weight: bold;
                            letter-spacing: 8px;
                            padding: 15px 25px;
                            background-color: #f8f9fa;
                            border-radius: 8px;
                            color: #2c3e50;
                            display: inline-block;
                        }
                        .footer {
                            padding: 20px;
                            text-align: center;
                            font-size: 12px;
                            color: #777777;
                            border-top: 1px solid #eeeeee;
                        }
                        .social-icons {
                            margin: 15px 0;
                        }
                        .social-icon {
                            display: inline-block;
                            margin: 0 10px;
                            width: 30px;
                            height: 30px;
                            background-color: #2c3e50;
                            border-radius: 50%;
                            color: white;
                            line-height: 30px;
                            text-align: center;
                        }
                        .note {
                            padding: 15px;
                            background-color: #f8f9fa;
                            border-left: 4px solid #e74c3c;
                            margin: 20px 0;
                        }
                        @media only screen and (max-width: 600px) {
                            .container {
                                width: 100%;
                            }
                            .otp-code {
                                font-size: 24px;
                            }
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <div class="logo">Stylic AI</div>
                        </div>
                        <div class="content">
                            <h2>Client Photoshoot generation failed</h2>
                            <p>Hello there,</p>
                            <p>Thank you for choosing Stylic AI! Please see what is the issue coming in """ + photoshoot_id + """</p>
                            <p>If you have any questions or need assistance, our customer support team is always here to help.</p>
                            <p>Best Regards,<br>The Quickoo Team</p>
                        </div>
                        <div class="footer">
                            <p>&copy; 2025 Quickoo. All rights reserved.</p>
                            <p>This is an automated message, please do not reply to this email.</p>
                        </div>
                    </div>
                </body>
                </html>
                """

            return photoshoot_faileur

        except Exception as e:
            (
                print(f"{datetime.now()}: Error in getting otp verification html format: {str(e)}"))

    def forgot_password_mail_template(self, reset_link):
        try:
            forgot_password = f"""
                <!DOCTYPE html>
                <html lang="en">

                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Reset Your Password - Stylic AI</title>
                    <style>
                        /* Reset styles */
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

                        .cta-container {{
                            text-align: center;
                            margin: 40px 0;
                        }}

                        .reset-button {{
                            display: inline-block;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: #ffffff;
                            text-decoration: none;
                            padding: 16px 32px;
                            border-radius: 50px;
                            font-weight: 600;
                            font-size: 16px;
                            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                            transition: all 0.3s ease;
                            border: none;
                            cursor: pointer;
                        }}

                        .reset-button:hover {{
                            transform: translateY(-2px);
                            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                        }}

                        .alternative-text {{
                            font-size: 14px;
                            color: #718096;
                            margin-top: 30px;
                            padding: 20px;
                            background-color: #f7fafc;
                            border-radius: 8px;
                            border-left: 4px solid #667eea;
                        }}

                        .alternative-link {{
                            color: #667eea;
                            word-break: break-all;
                            text-decoration: none;
                        }}

                        .security-note {{
                            background-color: #fef5e7;
                            border: 1px solid #f6ad55;
                            border-radius: 8px;
                            padding: 20px;
                            margin-top: 30px;
                        }}

                        .security-icon {{
                            color: #dd6b20;
                            font-size: 20px;
                            margin-right: 8px;
                        }}

                        .security-text {{
                            font-size: 14px;
                            color: #744210;
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

                        .footer-link:hover {{
                            color: #ffffff;
                        }}

                        .divider {{
                            height: 1px;
                            background: linear-gradient(to right, transparent, #e2e8f0, transparent);
                            margin: 30px 0;
                        }}

                        /* Responsive */
                        @media only screen and (max-width: 600px) {{
                            .email-container {{
                                margin: 0;
                                border-radius: 0;
                            }}

                            .header,
                            .content,
                            .footer {{
                                padding: 25px 20px;
                            }}

                            .header-title {{
                                font-size: 24px;
                            }}

                            .greeting {{
                                font-size: 18px;
                            }}

                            .reset-button {{
                                padding: 14px 28px;
                                font-size: 15px;
                            }}
                        }}
                    </style>
                </head>

                <body>
                    <div class="email-container">
                        <!-- Header -->
                        <div class="header">
                            <img src="https://app.stylic.ai/static/external/logo.png" alt="Stylic AI Logo" class="logo">
                            <h1 class="header-title">Password Reset</h1>
                        </div>

                        <!-- Content -->
                        <div class="content">
                            <div class="greeting">Hello there! 👋</div>

                            <div class="message">
                                We received a request to reset your password for your Stylic AI account. Don't worry, it happens to the
                                best of us! Click the button below to create a new password and get back to creating amazing content
                                with AI.
                            </div>

                            <div class="cta-container">
                                <a href="{reset_link}" class="reset-button">Reset My Password</a>
                            </div>

                            <div class="divider"></div>

                            <div class="alternative-text">
                                <strong>Button not working?</strong> Copy and paste this link into your browser:<br>
                                <a href="{reset_link}"
                                    class="alternative-link">{reset_link}</a>
                            </div>

                            <div class="security-note">
                                <div style="display: flex; align-items: flex-start;">
                                    <span class="security-icon">🔒</span>
                                    <div class="security-text">
                                        <strong>Security Note:</strong> This password reset link will expire in 24 hours for your
                                        security. If you didn't request this reset, please ignore this email or contact our support
                                        team.
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Footer -->
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
                                © 2025 Stylic AI. All rights reserved.<br>
                                If you no longer wish to receive these emails, you can unsubscribe
                                    here</a>.
                            </div>
                        </div>
                    </div>
                </body>

                </html>
            """
            return forgot_password

        except Exception as e:
            print(f"{datetime.now()}: Error in forgot password mail template: {e}")

    def welcome_user_mail(self, username):
        try:
            welcome_mail = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Welcome to Stylic AI!</title>
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
                            background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
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
                            font-size: 32px;
                            font-weight: 700;
                            margin: 0;
                            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                        }}
                        
                        .welcome-badge {{
                            background-color: rgba(255, 255, 255, 0.2);
                            color: #ffffff;
                            padding: 8px 16px;
                            border-radius: 20px;
                            font-size: 14px;
                            font-weight: 600;
                            margin-top: 15px;
                            display: inline-block;
                        }}
                        
                        .content {{
                            padding: 40px 30px;
                        }}
                        
                        .greeting {{
                            font-size: 24px;
                            color: #2d3748;
                            margin-bottom: 20px;
                            font-weight: 700;
                            text-align: center;
                        }}
                        
                        .message {{
                            font-size: 16px;
                            color: #4a5568;
                            margin-bottom: 30px;
                            line-height: 1.7;
                            text-align: center;
                        }}
                        
                        .features-container {{
                            background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
                            border-radius: 12px;
                            padding: 30px;
                            margin: 30px 0;
                        }}
                        
                        .features-title {{
                            font-size: 20px;
                            font-weight: 700;
                            color: #7c3aed;
                            margin-bottom: 20px;
                            text-align: center;
                        }}
                        
                        .feature-item {{
                            display: flex;
                            align-items: center;
                            margin-bottom: 15px;
                            padding: 15px;
                            background-color: #ffffff;
                            border-radius: 8px;
                            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                        }}
                        
                        .feature-icon {{
                            font-size: 24px;
                            margin-right: 15px;
                            min-width: 40px;
                        }}
                        
                        .feature-text {{
                            flex: 1;
                        }}
                        
                        .feature-title {{
                            font-weight: 600;
                            color: #2d3748;
                            margin-bottom: 5px;
                        }}
                        
                        .feature-desc {{
                            font-size: 14px;
                            color: #6b7280;
                        }}
                        
                        .cta-container {{
                            text-align: center;
                            margin: 40px 0;
                        }}
                        
                        .cta-button {{
                            display: inline-block;
                            background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
                            color: #ffffff;
                            text-decoration: none;
                            padding: 16px 32px;
                            border-radius: 50px;
                            font-weight: 600;
                            font-size: 16px;
                            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
                            transition: all 0.3s ease;
                        }}
                        
                        .cta-button:hover {{
                            transform: translateY(-2px);
                            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6);
                        }}
                        
                        .tips-section {{
                            background-color: #f0f9ff;
                            border: 1px solid #0ea5e9;
                            border-radius: 8px;
                            padding: 25px;
                            margin-top: 30px;
                        }}
                        
                        .tips-title {{
                            color: #0369a1;
                            font-weight: 600;
                            margin-bottom: 15px;
                            display: flex;
                            align-items: center;
                        }}
                        
                        .tips-icon {{
                            margin-right: 8px;
                            font-size: 20px;
                        }}
                        
                        .tips-list {{
                            color: #1e40af;
                            font-size: 14px;
                            line-height: 1.6;
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
                        
                        .footer-link:hover {{
                            color: #ffffff;
                        }}
                        
                        @media only screen and (max-width: 600px) {{
                            .email-container {{
                                margin: 0;
                                border-radius: 0;
                            }}
                            
                            .header, .content, .footer {{
                                padding: 25px 20px;
                            }}
                            
                            .header-title {{
                                font-size: 26px;
                            }}
                            
                            .greeting {{
                                font-size: 20px;
                            }}
                            
                            .feature-item {{
                                flex-direction: column;
                                text-align: center;
                            }}
                            
                            .feature-icon {{
                                margin-right: 0;
                                margin-bottom: 10px;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <img src="https://app.stylic.ai/static/external/logo.png" alt="Stylic AI Logo" class="logo">
                            <h1 class="header-title">Welcome Aboard!</h1>
                            <div class="welcome-badge">🎉 New Member</div>
                        </div>
                        
                        <div class="content">
                            <div class="greeting">Hello {username}! 👋</div>
                            
                            <div class="message">
                                We're thrilled to welcome you to the Stylic AI family! You've just joined thousands of creators who are transforming their ideas into stunning visuals with the power of AI.
                            </div>
                            
                            <div class="features-container">
                                <div class="features-title">What you can do with Stylic AI:</div>
                                
                                <div class="feature-item">
                                    <div class="feature-icon">🎨</div>
                                    <div class="feature-text">
                                        <div class="feature-title">AI-Powered Photoshoot</div>
                                        <div class="feature-desc">Create stunning your garment AI photoshoot in seconds</div>
                                    </div>
                                </div>
                                
                                <div class="feature-item">
                                    <div class="feature-icon">⚡</div>
                                    <div class="feature-text">
                                        <div class="feature-title">Lightning Fast</div>
                                        <div class="feature-desc">Generate professional designs faster than ever before</div>
                                    </div>
                                </div>
                                
                                <div class="feature-item">
                                    <div class="feature-icon">🚀</div>
                                    <div class="feature-text">
                                        <div class="feature-title">Easy to Use</div>
                                        <div class="feature-desc">No design experience needed - just upload what you want</div>
                                    </div>
                                </div>
                                
                                <div class="feature-item">
                                    <div class="feature-icon">💎</div>
                                    <div class="feature-text">
                                        <div class="feature-title">Premium Quality</div>
                                        <div class="feature-desc">High-resolution outputs perfect for any project</div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="cta-container">
                                <a href="https://app.stylic.ai/ai-photoshoot" class="cta-button">Start Creating Now</a>
                            </div>
                            
                            <div class="tips-section">
                                <div class="tips-title">
                                    <span class="tips-icon">💡</span>
                                    Quick Tips to Get Started:
                                </div>
                                <div class="tips-list">
                                    • Be specific in your garment for better results<br>
                                    • Try different styles and poses to explore possibilities<br>
                                    • Save your favorite creations to your gallery<br>
                                    • Check out our tutorials and community showcase<br>
                                    • Need help? Our support team is here 24/7
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
                                © 2025 Stylic AI. All rights reserved.<br>
                                If you no longer wish to receive these emails, you can unsubscribe
                                    here</a>.
                            </div>
                        </div>
                    </div>
                </body>
                </html>
            """

            return welcome_mail

        except Exception as e:
            print(f"Error in sending welcome user mail: {e}")

    def invoice_sending(self, mapping_dict, customer_name):
        try:
            invoice_id = mapping_dict["id"]
            email = session.get("login_dict", {}).get("email", "")
            today = datetime.today()
            payment_date = today.strftime("%d-%m-%Y")
            payment_method = "razorpay"
            payment_id = mapping_dict["payment_id"]
            paid_amount = f"{mapping_dict['amount']} {mapping_dict['currency']}"
            invoice_url = mapping_dict["invoice_url"]

            payment_invoice = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Payment Confirmation - Stylic AI</title>
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
                            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                            padding: 40px 30px;
                            text-align: center;
                            border-radius: 8px 8px 0 0;
                        }}
                        
                        .logo {{
                            max-width: 150px;
                            height: auto;
                            margin-bottom: 20px;
                        }}
                        
                        .success-icon {{
                            width: 80px;
                            height: 80px;
                            background-color: rgba(255, 255, 255, 0.2);
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            margin: 0 auto 20px;
                            font-size: 40px;
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
                        }}
                        
                        .greeting {{
                            font-size: 20px;
                            color: #2d3748;
                            margin-bottom: 20px;
                            font-weight: 600;
                            text-align: center;
                        }}
                        
                        .message {{
                            font-size: 16px;
                            color: #4a5568;
                            margin-bottom: 30px;
                            line-height: 1.7;
                            text-align: center;
                        }}
                        
                        .invoice-container {{
                            background-color: #f8fafc;
                            border: 1px solid #e2e8f0;
                            border-radius: 12px;
                            padding: 30px;
                            margin: 30px 0;
                        }}
                        
                        .invoice-header {{
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            margin-bottom: 25px;
                            padding-bottom: 15px;
                            border-bottom: 2px solid #e2e8f0;
                        }}
                        
                        .invoice-title {{
                            font-size: 22px;
                            font-weight: 700;
                            color: #2d3748;
                        }}
                        
                        .invoice-number {{
                            font-size: 14px;
                            color: #6b7280;
                            background-color: #ffffff;
                            padding: 8px 12px;
                            border-radius: 6px;
                            font-family: 'Courier New', monospace;
                        }}
                        
                        .invoice-details {{
                            margin-bottom: 25px;
                        }}
                        
                        .detail-row {{
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            padding: 12px 0;
                            border-bottom: 1px solid #f1f5f9;
                        }}
                        
                        .detail-row:last-child {{
                            border-bottom: none;
                        }}
                        
                        .detail-label {{
                            font-size: 14px;
                            color: #6b7280;
                            font-weight: 500;
                        }}
                        
                        .detail-value {{
                            font-size: 14px;
                            color: #2d3748;
                            font-weight: 600;
                        }}
                        
                        .plan-info {{
                            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                            border: 1px solid #0ea5e9;
                            border-radius: 8px;
                            padding: 20px;
                            margin: 20px 0;
                        }}
                        
                        .plan-title {{
                            font-size: 18px;
                            font-weight: 700;
                            color: #0c4a6e;
                            margin-bottom: 10px;
                        }}
                        
                        .plan-features {{
                            font-size: 14px;
                            color: #0369a1;
                            line-height: 1.6;
                        }}
                        
                        .total-section {{
                            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
                            border: 2px solid #10b981;
                            border-radius: 10px;
                            padding: 20px;
                            margin-top: 20px;
                        }}
                        
                        .total-row {{
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                        }}
                        
                        .total-label {{
                            font-size: 18px;
                            font-weight: 700;
                            color: #059669;
                        }}
                        
                        .total-amount {{
                            font-size: 24px;
                            font-weight: 700;
                            color: #059669;
                        }}
                        
                        .next-steps {{
                            background-color: #fef7ff;
                            border: 1px solid #d8b4fe;
                            border-radius: 10px;
                            padding: 25px;
                            margin: 30px 0;
                        }}
                        
                        .next-steps-title {{
                            font-size: 18px;
                            font-weight: 600;
                            color: #7c3aed;
                            margin-bottom: 15px;
                            display: flex;
                            align-items: center;
                        }}
                        
                        .next-steps-icon {{
                            margin-right: 8px;
                            font-size: 20px;
                        }}
                        
                        .next-steps-list {{
                            color: #6b46c1;
                            font-size: 14px;
                            line-height: 1.8;
                        }}
                        
                        .cta-container {{
                            text-align: center;
                            margin: 40px 0;
                        }}
                        
                        .cta-button {{
                            display: inline-block;
                            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                            color: #ffffff;
                            text-decoration: none;
                            padding: 16px 32px;
                            border-radius: 50px;
                            font-weight: 600;
                            font-size: 16px;
                            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
                            transition: all 0.3s ease;
                            margin: 0 10px 10px 0;
                        }}
                        
                        .cta-button:hover {{
                            transform: translateY(-2px);
                            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6);
                        }}
                        
                        .cta-button.secondary {{
                            background: transparent;
                            color: #10b981;
                            border: 2px solid #10b981;
                            box-shadow: none;
                        }}
                        
                        .cta-button.secondary:hover {{
                            background-color: #10b981;
                            color: #ffffff;
                        }}
                        
                        .support-note {{
                            background-color: #f0f9ff;
                            border: 1px solid #0ea5e9;
                            border-radius: 8px;
                            padding: 20px;
                            margin-top: 30px;
                            text-align: center;
                        }}
                        
                        .support-text {{
                            font-size: 14px;
                            color: #0369a1;
                            line-height: 1.6;
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
                        
                        .footer-link:hover {{
                            color: #ffffff;
                        }}
                        
                        @media only screen and (max-width: 600px) {{
                            .email-container {{
                                margin: 0;
                                border-radius: 0;
                            }}
                            
                            .header, .content, .footer {{
                                padding: 25px 20px;
                            }}
                            
                            .header-title {{
                                font-size: 24px;
                            }}
                            
                            .invoice-header {{
                                flex-direction: column;
                                text-align: center;
                                gap: 15px;
                            }}
                            
                            .detail-row {{
                                flex-direction: column;
                                align-items: flex-start;
                                gap: 5px;
                            }}
                            
                            .total-row {{
                                flex-direction: column;
                                gap: 10px;
                                text-align: center;
                            }}
                            
                            .cta-button {{
                                display: block;
                                margin: 10px 0;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <img src="https://app.stylic.ai/static/external/logo.png" alt="Stylic AI Logo" class="logo">
                            <div class="success-icon">✅</div>
                            <h1 class="header-title">Payment Successful!</h1>
                        </div>
                        
                        <div class="content">
                            <div class="greeting">Thank you for your purchase! 🎉</div>
                            
                            <div class="message">
                                Your payment has been processed successfully. You now have access to all premium features and your credit was credited. Here are your payment details:
                            </div>
                            
                            <div class="invoice-container">
                                <div class="invoice-header">
                                    <div class="invoice-title">Invoice</div>
                                    <div class="invoice-number">{invoice_id}</div>
                                </div>
                                
                                <div class="invoice-details">
                                    <div class="detail-row">
                                        <div class="detail-label">Customer Name:</div>
                                        <div class="detail-value">{customer_name}</div>
                                    </div>
                                    <div class="detail-row">
                                        <div class="detail-label">Email:</div>
                                        <div class="detail-value">{email}</div>
                                    </div>
                                    <div class="detail-row">
                                        <div class="detail-label">Payment Date:</div>
                                        <div class="detail-value">{payment_date}</div>
                                    </div>
                                    <div class="detail-row">
                                        <div class="detail-label">Payment Method:</div>
                                        <div class="detail-value">{payment_method}</div>
                                    </div>
                                    <div class="detail-row">
                                        <div class="detail-label">Transaction ID:</div>
                                        <div class="detail-value">{payment_id}</div>
                                    </div>
                                </div>
                                
                                <div class="plan-info">
                                    <div class="plan-title">Stylic AI Premium Features</div>
                                    <div class="plan-features">
                                        ✓ Apparel AI Photoshoot<br>
                                        ✓ AI Video Generation<br>
                                        ✓ Product Photoshoot<br>
                                        ✓ AI Human Model Generation<br>
                                        ✓ Background Replacer<br>
                                        ✓ Image Upscaler & Enhancer
                                    </div>
                                </div>
                                
                                <div class="total-section">
                                    <div class="total-row">
                                        <div class="total-label">Total Paid:</div>
                                        <div class="total-amount">{paid_amount}</div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="next-steps">
                                <div class="next-steps-title">
                                    <span class="next-steps-icon">🚀</span>
                                    What's Next?
                                </div>
                                <div class="next-steps-list">
                                    • Your premium features are now active and ready to use<br>
                                    • Open your user panel and use whatever featire you want to use<br>
                                    • Just like upload your product and AI makes magics for you<br>
                                    • Join our social media for checkout latest news and update<br>
                                </div>
                            </div>
                            
                            <div class="cta-container">
                                <a href="https://app.stylic.ai/" class="cta-button">Start Creating</a>
                                <a href="{invoice_url}" class="cta-button secondary">Download Invoice</a>
                            </div>
                            
                            <div class="support-note">
                                <div class="support-text">
                                    <strong>Need help?</strong> Our support team is here for you 24/7. If you have any questions about your subscription or need assistance, don't hesitate to reach out to us.
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
                                © 2025 Stylic AI. All rights reserved.<br>
                                If you no longer wish to receive these emails, you can unsubscribe
                                    here</a>.
                            </div>
                        </div>
                    </div>
                </body>
                </html>
            """

            return payment_invoice

        except Exception as e:
            print(f"{datetime.utcnow()}: Error in invoice html template: {e}")
