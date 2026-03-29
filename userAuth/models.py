from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    last_seen_bookings_at = models.DateTimeField(null=True, blank=True)
    booking_terms_accepted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.email

    @property
    def has_accepted_booking_terms(self):
        return self.booking_terms_accepted_at is not None

    def mark_booking_terms_accepted(self):
        if not self.booking_terms_accepted_at:
            self.booking_terms_accepted_at = timezone.now()
            self.save(update_fields=["booking_terms_accepted_at"])
