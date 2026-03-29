from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Booking(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
        ("expired", "Expired"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    car = models.ForeignKey(
        "cars.Car",
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    pick_up_location = models.CharField(max_length=255)
    drop_off_location = models.CharField(max_length=255)

    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()

    drop_off_date = models.DateField()
    drop_off_time = models.TimeField()

    driver_required = models.BooleanField(default=False)
    additional_notes = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["car", "pick_up_date"]),
        ]

    def __str__(self):
        user_label = self.user.email if self.user_id and hasattr(self.user, "email") else "No user"
        car_label = self.car.name if self.car_id and hasattr(self.car, "name") else "No car"
        return f"Booking #{self.id} - {user_label} - {car_label}"

    def clean(self):
        """Validate booking dates, times, and prevent overbooking."""
        if not all(
            [
                self.pick_up_date,
                self.drop_off_date,
                self.pick_up_time,
                self.drop_off_time,
            ]
        ):
            return

        today = timezone.now().date()

        if self.pick_up_date < today:
            raise ValidationError("Pick-up date cannot be in the past")

        if self.drop_off_date < self.pick_up_date:
            raise ValidationError("Drop-off date must be after pick-up date")

        if self.drop_off_date == self.pick_up_date and self.drop_off_time <= self.pick_up_time:
            raise ValidationError("Drop-off time must be after pick-up time for same-day rentals")

        if self.car_id is None:
            return

        conflicting_bookings = Booking.objects.filter(
            car=self.car,
            status__in=["confirmed", "completed"],
            is_deleted=False,
        ).exclude(id=self.id if self.id else None)

        for booking in conflicting_bookings:
            if not (
                self.drop_off_date < booking.pick_up_date
                or self.pick_up_date > booking.drop_off_date
            ):
                raise ValidationError(
                    f"Car is already booked from {booking.pick_up_date} to {booking.drop_off_date}"
                )

    def save(self, *args, **kwargs):
        """Run validations before saving."""
        self.full_clean()
        super().save(*args, **kwargs)

    def get_duration(self):
        """Calculate booking duration in days."""
        delta = self.drop_off_date - self.pick_up_date
        return max(delta.days, 1)

    @property
    def duration_days(self):
        """Duration in days for templates."""
        return self.get_duration()

    def get_total_price(self):
        """Calculate total price based on duration and daily rate."""
        duration = self.get_duration()
        return self.car.price_per_day * duration

    @property
    def total_price(self):
        """Total price for templates."""
        return self.get_total_price()

    def is_valid_status_transition(self, new_status):
        """Prevent invalid status transitions."""
        valid_transitions = {
            "draft": ["confirmed", "cancelled"],
            "confirmed": ["cancelled", "completed"],
            "cancelled": [],
            "completed": [],
            "expired": [],
        }
        return new_status in valid_transitions.get(self.status, [])

    def soft_delete(self):
        """Mark as deleted without removing from database."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
