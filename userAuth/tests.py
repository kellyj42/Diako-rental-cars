from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from unittest.mock import patch

from userAuth.tokens import email_verification_token


class EmailVerificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="newuser@example.com",
            email="newuser@example.com",
            password="StrongPass123",
        )
        self.user.profile.is_verified = False
        self.user.profile.save()

    def test_verify_email_rejects_invalid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        response = self.client.get(
            reverse("userAuth:verify_email", kwargs={"uidb64": uid, "token": "invalid-token"})
        )

        self.user.refresh_from_db()
        self.assertFalse(self.user.profile.is_verified)
        self.assertRedirects(response, reverse("userAuth:email_verification"))

    def test_verify_email_accepts_valid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = email_verification_token.make_token(self.user)

        response = self.client.get(
            reverse("userAuth:verify_email", kwargs={"uidb64": uid, "token": token})
        )

        self.user.refresh_from_db()
        self.assertTrue(self.user.profile.is_verified)
        self.assertRedirects(response, reverse("userAuth:login"))

    def test_resend_verification_requires_pending_user(self):
        response = self.client.post(reverse("userAuth:resend_verification"))

        self.assertRedirects(response, reverse("userAuth:login"))

    def test_resend_verification_uses_session_user(self):
        session = self.client.session
        session["verify_user_id"] = self.user.id
        session["verify_email"] = self.user.email
        session.save()

        with patch("userAuth.views.send_verification_email") as mock_send:
            response = self.client.post(reverse("userAuth:resend_verification"))

        self.assertRedirects(response, reverse("userAuth:email_verification"))
        mock_send.assert_called_once()
