"""Celery background tasks."""
import logging
from .celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.send_verification_email")
def send_verification_email(email: str, otp_code: str):
    """Send verification email with OTP code to user.

    Args:
        email: User's email address
        otp_code: 6-digit OTP code for verification
    """
    # TODO: Implement actual email sending logic
    # For now, just log the email details
    logger.info(f"Sending verification email to {email} with code: {otp_code}")

    # Example of what this should do:
    # 1. Create email template with OTP code
    # 2. Send via SMTP/email service (SendGrid, AWS SES, etc.)
    # 3. Log success/failure

    print(f"📧 Verification email sent to {email} with code: {otp_code}")
    return {"status": "sent", "email": email}
