from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Token only changes when verification state changes
        return f"{user.pk}{timestamp}{user.profile.is_verified}"

email_verification_token = EmailVerificationTokenGenerator()
