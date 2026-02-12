from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from userAuth.tokens import email_verification_token

def send_verification_email(request, user):
    token = email_verification_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    verification_link = request.build_absolute_uri(
        reverse("userAuth:verify_email", kwargs={"uidb64": uid, "token": token})
    )

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=user.email,
        subject="Verify your email address",
        html_content=f"""
            <h2>Welcome to Diako Rental Cars</h2>
            <p>Please click the link below to verify your email:</p>
            <a href="{verification_link}">Verify Email</a>
        """,
    )

    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(message)
