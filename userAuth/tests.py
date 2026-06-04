from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from unittest.mock import patch

from django.contrib.auth.tokens import default_token_generator
from userAuth.tokens import email_verification_token


TEST_STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


@override_settings(STORAGES=TEST_STORAGES)
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


@override_settings(STORAGES=TEST_STORAGES)
class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reset@example.com",
            email="reset@example.com",
            password="OldStrongPass123!",
        )

    def test_password_reset_request_sends_email_for_existing_user(self):
        with patch("userAuth.views.send_password_reset_email") as mock_send:
            response = self.client.post(
                reverse("userAuth:password_reset_link"),
                {"email": self.user.email},
            )

        self.assertRedirects(response, reverse("userAuth:password_reset_done"))
        mock_send.assert_called_once()

    def test_password_reset_request_rejects_unknown_email(self):
        with patch("userAuth.views.send_password_reset_email") as mock_send:
            response = self.client.post(
                reverse("userAuth:password_reset_link"),
                {"email": "missing@example.com"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No account was found with that email address.")
        self.assertContains(response, "missing@example.com")
        mock_send.assert_not_called()

    def test_valid_password_reset_token_renders_form(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        response = self.client.get(
            reverse("userAuth:reset_password_confirm", kwargs={"uidb64": uid, "token": token})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create New Password")
        self.assertContains(response, 'name="new_password1"')
        self.assertContains(response, 'name="new_password2"')

    def test_valid_password_reset_token_changes_password(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        response = self.client.post(
            reverse("userAuth:reset_password_confirm", kwargs={"uidb64": uid, "token": token}),
            {
                "new_password1": "NewStrongPass123!",
                "new_password2": "NewStrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("userAuth:login"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewStrongPass123!"))

    def test_invalid_password_reset_token_redirects_to_request_form(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        response = self.client.get(
            reverse("userAuth:reset_password_confirm", kwargs={"uidb64": uid, "token": "bad-token"})
        )

        self.assertRedirects(response, reverse("userAuth:password_reset_link"))
