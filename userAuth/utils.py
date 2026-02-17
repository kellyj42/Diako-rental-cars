from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from userAuth.tokens import email_verification_token
from content.content import contact_info

def send_verification_email(request, user):
    token = email_verification_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    verification_link = request.build_absolute_uri(
        reverse("userAuth:verify_email", kwargs={"uidb64": uid, "token": token})
    )

    support_email = contact_info["email"]["support"]

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=user.email,
        subject="Verify your email address",
        html_content=f"""
                        <div style="background-color:#f5f7fb;padding:32px 0;font-family:Arial,sans-serif;">
                            <div style="max-width:600px;margin:0 auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 10px 30px rgba(15,23,42,0.08);">
                                <div style="background:linear-gradient(90deg,#1e3a8a,#1d4ed8);padding:18px 24px;">
                                    <h1 style="margin:0;color:#ffffff;font-size:20px;letter-spacing:0.5px;">Diako Rental Cars</h1>
                                </div>

                                <div style="padding:28px 32px;color:#0f172a;">
                                    <p style="margin:0 0 12px;font-size:14px;color:#64748b;">Hi {user.first_name or user.username},</p>
                                    <h2 style="margin:0 0 12px;font-size:24px;color:#0f172a;">Verify your email to get started</h2>
                                    <p style="margin:0 0 18px;line-height:1.6;color:#475569;">
                                        Thanks for choosing Diako Rental Cars. Click the button below to verify your email address and complete your account setup.
                                    </p>

                                    <div style="text-align:center;margin:24px 0 28px;">
                                        <a href="{verification_link}"
                                             style="display:inline-block;background:#f97316;color:#ffffff;text-decoration:none;padding:12px 24px;border-radius:999px;font-weight:600;">
                                            Verify Email
                                        </a>
                                    </div>

                                    <p style="margin:0 0 8px;color:#64748b;font-size:13px;">This link will expire in 5 minutes.</p>
                                    <p style="margin:0;color:#64748b;font-size:13px;">If you didn’t create an account, you can safely ignore this email.</p>

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
        """,
    )

    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(message)
