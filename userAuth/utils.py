import logging

from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from content.content import contact_info
from userAuth.tokens import email_verification_token

logger = logging.getLogger(__name__)


def send_verification_email(request, user):
    token = email_verification_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_path = reverse("userAuth:verify_email", kwargs={"uidb64": uid, "token": token})

    if settings.APP_BASE_URL:
        verification_link = f"{settings.APP_BASE_URL.rstrip('/')}{verification_path}"
    else:
        verification_link = request.build_absolute_uri(verification_path)

    support_email = contact_info["email"]["support"]
    html_content = f"""
        <div style="background-color:#f5f7fb;padding:32px 0;font-family:Arial,sans-serif;">
            <div style="max-width:600px;margin:0 auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 10px 30px rgba(15,23,42,0.08);">
                <div style="background:linear-gradient(90deg,#1e3a8a,#1d4ed8);padding:18px 24px;">
                    <h1 style="margin:0;color:#ffffff;font-size:20px;letter-spacing:0.5px;">Daiko Travel Agency Ltd</h1>
                </div>

                <div style="padding:28px 32px;color:#0f172a;">
                    <p style="margin:0 0 12px;font-size:14px;color:#64748b;">Hi {user.first_name or user.username},</p>
                    <h2 style="margin:0 0 12px;font-size:24px;color:#0f172a;">Verify your email to get started</h2>
                    <p style="margin:0 0 18px;line-height:1.6;color:#475569;">
                        Thanks for choosing Daiko Travel Agency Ltd. Click the button below to verify your email address and complete your account setup.
                    </p>

                    <div style="text-align:center;margin:24px 0 28px;">
                        <a href="{verification_link}"
                           style="display:inline-block;background:#f97316;color:#ffffff;text-decoration:none;padding:12px 24px;border-radius:999px;font-weight:600;">
                            Verify Email
                        </a>
                    </div>

                    <p style="margin:0 0 8px;color:#64748b;font-size:13px;">This link will expire in 5 minutes.</p>
                    <p style="margin:0;color:#64748b;font-size:13px;">If you did not create an account, you can safely ignore this email.</p>

                    <div style="margin-top:24px;padding:12px 16px;background:#f8fafc;border-radius:12px;color:#64748b;font-size:12px;">
                        Trouble with the button? Copy and paste this URL into your browser:<br/>
                        <span style="word-break:break-all;color:#2563eb;">{verification_link}</span>
                    </div>
                </div>

                <div style="border-top:1px solid #e2e8f0;padding:16px 24px;text-align:center;color:#94a3b8;font-size:12px;">
                    Need help? Contact us at {support_email}
                </div>
            </div>
        </div>
    """

    if not settings.SENDGRID_API_KEY:
        logger.warning(
            "SENDGRID_API_KEY is not configured. Verification email not sent for user %s. Verification link: %s",
            user.email,
            verification_link,
        )
        return False

    try:
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=user.email,
            subject="Verify your email address",
            html_content=html_content,
        )
        SendGridAPIClient(settings.SENDGRID_API_KEY).send(message)
        return True
    except Exception:
        logger.exception(
            "Failed to send verification email for user %s. Verification link: %s",
            user.email,
            verification_link,
        )
        return False
