from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    last_seen_bookings_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.email
