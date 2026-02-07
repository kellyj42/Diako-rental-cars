from django.db import models
from django.conf import settings

class Booking(models.Model):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    car = models.ForeignKey("cars.Car", on_delete=models.CASCADE)

    pick_up_location = models.CharField(max_length=255)
    drop_off_location = models.CharField(max_length=255)

    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()

    drop_off_date = models.DateField()
    drop_off_time = models.TimeField()

    additional_notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.car} | {self.pick_up_date} | {self.status}"
