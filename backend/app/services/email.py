"""Email service"""
import secrets
from datetime import datetime, timedelta
from app.config import settings

try:
    from resend import Resend
except ImportError:
    Resend = None


class EmailService:
    """Email service using Resend API"""

    def __init__(self):
        if not Resend:
            raise RuntimeError("Resend package is not installed")
        self.client = Resend(api_key=settings.RESEND_API_KEY)

    async def send_verification_email(self, email: str, verification_token: str) -> bool:
        """Send verification email"""
        verification_url = f"{settings.APP_URL}/verify-email?token={verification_token}"

        try:
            response = self.client.emails.send(
                {
                    "from": settings.FROM_EMAIL,
                    "to": email,
                    "subject": "Verify your Zattar email address",
                    "html": f"""
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2>Welcome to Zattar!</h2>
                        <p>Thank you for creating an account. Please verify your email address to get started.</p>
                        
                        <div style="margin: 30px 0; text-align: center;">
                            <a href="{verification_url}" 
                               style="background-color: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                                Verify Email Address
                            </a>
                        </div>
                        
                        <p>Or copy and paste this link in your browser:</p>
                        <p style="word-break: break-all; color: #666;">{verification_url}</p>
                        
                        <p style="margin-top: 30px; color: #999; font-size: 12px;">
                            This link will expire in 24 hours.
                        </p>
                        
                        <p style="color: #999; font-size: 12px;">
                            If you didn't create this account, please ignore this email.
                        </p>
                    </div>
                    """,
                }
            )
            return True
        except Exception as e:
            print(f"Error sending verification email: {e}")
            return False

    async def send_password_reset_email(self, email: str, reset_token: str) -> bool:
        """Send password reset email"""
        reset_url = f"{settings.APP_URL}/reset-password?token={reset_token}"

        try:
            response = self.client.emails.send(
                {
                    "from": settings.FROM_EMAIL,
                    "to": email,
                    "subject": "Reset your Zattar password",
                    "html": f"""
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2>Password Reset Request</h2>
                        <p>We received a request to reset your password. Click the button below to create a new password.</p>
                        
                        <div style="margin: 30px 0; text-align: center;">
                            <a href="{reset_url}" 
                               style="background-color: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                                Reset Password
                            </a>
                        </div>
                        
                        <p>Or copy and paste this link in your browser:</p>
                        <p style="word-break: break-all; color: #666;">{reset_url}</p>
                        
                        <p style="margin-top: 30px; color: #999; font-size: 12px;">
                            This link will expire in 1 hour.
                        </p>
                        
                        <p style="color: #999; font-size: 12px;">
                            If you didn't request this, please ignore this email.
                        </p>
                    </div>
                    """,
                }
            )
            return True
        except Exception as e:
            print(f"Error sending password reset email: {e}")
            return False


def generate_verification_token() -> str:
    """Generate a secure verification token"""
    return secrets.token_urlsafe(32)


email_service = EmailService()
