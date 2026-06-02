from datetime import time
import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Booking


DEFAULT_PICK_UP_TIME = time(8, 0)
DEFAULT_DROP_OFF_TIME = time(18, 0)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "pick_up_location",
            "drop_off_location",
            "pick_up_date",
            "drop_off_date",
            "additional_notes",
        ]

    agree_terms = forms.BooleanField(required=True, label="I agree to rental terms")

    def __init__(self, *args, require_terms=True, **kwargs):
        super().__init__(*args, **kwargs)
        if not require_terms:
            self.fields.pop("agree_terms", None)

    def clean_pick_up_location(self):
        return self._clean_location("pick_up_location", "Pickup")

    def clean_drop_off_location(self):
        return self._clean_location("drop_off_location", "Drop-off")

    def _clean_location(self, field_name, label):
        value = self.cleaned_data.get(field_name, "").strip()

        if not value:
            raise ValidationError(f"{label} location is required")

        if len(value) < 3:
            raise ValidationError(f"{label} location too short (minimum 3 characters)")

        if len(value) > 255:
            raise ValidationError(f"{label} location too long (maximum 255 characters)")

        location_pattern = re.compile(r"^[A-Za-z0-9\s\-\,\.\#]+$")
        if not location_pattern.match(value):
            raise ValidationError(
                "Location contains invalid characters. Use letters, numbers, hyphens, commas, or periods."
            )

        if re.search(r"<[^>]*>|javascript:|onclick|onerror|on\w+=", value, re.I):
            raise ValidationError("Location contains invalid content")

        return value

    def clean_additional_notes(self):
        text = self.cleaned_data.get("additional_notes", "").strip()

        if not text:
            return text

        if len(text) > 1000:
            raise ValidationError("Notes must be less than 1000 characters")

        if re.search(r"<[^>]*>", text):
            raise ValidationError("HTML tags are not allowed in notes")

        if re.search(r"javascript:|onclick|onerror|on\w+=", text, re.I):
            raise ValidationError("Suspicious content detected in notes")

        if re.search(r"(.)\1{20,}", text):
            raise ValidationError("Spam pattern detected - too many repeated characters")

        if not all(char.isprintable() or char in "\n\t" for char in text):
            raise ValidationError("Invalid characters detected in notes")

        return text

    def clean(self):
        data = super().clean()

        pick_date = data.get("pick_up_date")
        drop_date = data.get("drop_off_date")

        if not all([pick_date, drop_date]):
            return data

        today = timezone.now().date()

        if pick_date < today:
            raise ValidationError("Pick-up date cannot be in the past")

        if drop_date < pick_date:
            raise ValidationError("Drop-off date must be after pick-up date")

        days_diff = (drop_date - pick_date).days
        if days_diff > 90:
            raise ValidationError("Maximum rental period is 90 days")

        return data

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.pick_up_time = DEFAULT_PICK_UP_TIME
        booking.drop_off_time = DEFAULT_DROP_OFF_TIME

        if commit:
            booking.save()
            self.save_m2m()

        return booking
