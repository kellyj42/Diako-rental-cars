from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
import re
from .models import Booking


class BookingForm(forms.ModelForm):

    # -------------------------
    # CORE FIELDS
    # -------------------------

    class Meta:
        model = Booking
        fields = [
            "pick_up_location",
            "drop_off_location",
            "pick_up_date",
            "pick_up_time",
            "drop_off_date",
            "drop_off_time",
            "driver_required",
            "additional_notes",
        ]

    agree_terms = forms.BooleanField(required=True, label="I agree to rental terms")

    def __init__(self, *args, require_terms=True, **kwargs):
        super().__init__(*args, **kwargs)
        if not require_terms:
            self.fields.pop("agree_terms", None)

    # -------------------------
    # LOCATION VALIDATION ✅ FIX #24: Better regex for real addresses
    # -------------------------

    def clean_pick_up_location(self):
        """✅ FIX #24: Validate location format - allow numbers, letters, address characters"""
        value = self.cleaned_data.get("pick_up_location", "").strip()

        if not value:
            raise ValidationError("Pickup location is required")

        if len(value) < 3:
            raise ValidationError("Pickup location too short (minimum 3 characters)")

        if len(value) > 255:
            raise ValidationError("Pickup location too long (maximum 255 characters)")

        # ✅ FIX #24: Allow numbers and common address characters
        # Pattern: letters, numbers, spaces, hyphens, commas, periods, # for apartment numbers
        location_pattern = re.compile(r"^[A-Za-z0-9\s\-\,\.\#]+$")
        
        if not location_pattern.match(value):
            raise ValidationError(
                "Location contains invalid characters. Use letters, numbers, hyphens, commas, or periods."
            )

        # Block dangerous patterns (XSS prevention)
        if re.search(r'<[^>]*>|javascript:|onclick|onerror|on\w+=', value, re.I):
            raise ValidationError("Location contains invalid content")

        return value

    def clean_drop_off_location(self):
        """Same validation as pick_up_location"""
        value = self.cleaned_data.get("drop_off_location", "").strip()

        if not value:
            raise ValidationError("Drop-off location is required")

        if len(value) < 3:
            raise ValidationError("Drop-off location too short (minimum 3 characters)")

        if len(value) > 255:
            raise ValidationError("Drop-off location too long (maximum 255 characters)")

        location_pattern = re.compile(r"^[A-Za-z0-9\s\-\,\.\#]+$")
        
        if not location_pattern.match(value):
            raise ValidationError(
                "Location contains invalid characters. Use letters, numbers, hyphens, commas, or periods."
            )

        if re.search(r'<[^>]*>|javascript:|onclick|onerror|on\w+=', value, re.I):
            raise ValidationError("Location contains invalid content")

        return value

    # -------------------------
    # TEXTAREA SECURITY
    # -------------------------

    def clean_additional_notes(self):
        """Sanitize notes for XSS prevention"""
        text = self.cleaned_data.get("additional_notes", "").strip()

        if not text:
            return text

        if len(text) > 1000:
            raise ValidationError("Notes must be less than 1000 characters")

        # Block HTML tags
        if re.search(r'<[^>]*>', text):
            raise ValidationError("HTML tags are not allowed in notes")

        # Block script patterns
        if re.search(r'javascript:|onclick|onerror|on\w+=', text, re.I):
            raise ValidationError("Suspicious content detected in notes")

        # Check for spam character floods
        if re.search(r"(.)\1{20,}", text):
            raise ValidationError("Spam pattern detected - too many repeated characters")

        # Ensure printable characters
        if not all(c.isprintable() or c in '\n\t' for c in text):
            raise ValidationError("Invalid characters detected in notes")

        return text

    # -------------------------
    # DATE & TIME LOGIC VALIDATION ✅ FIX #10, #22
    # -------------------------

    def clean(self):
        """✅ FIX #10: Comprehensive date/time validation"""
        data = super().clean()

        pick_date = data.get("pick_up_date")
        pick_time = data.get("pick_up_time")
        drop_date = data.get("drop_off_date")
        drop_time = data.get("drop_off_time")

        if not all([pick_date, drop_date, pick_time, drop_time]):
            return data

        today = timezone.now().date()

        # Check pick-up date is not in past
        if pick_date < today:
            raise ValidationError("Pick-up date cannot be in the past")

        # Check drop-off date is after pick-up date
        if drop_date < pick_date:
            raise ValidationError("Drop-off date must be after pick-up date")

        # ✅ FIX #10: Validate times for same-day rentals
        if pick_date == drop_date:
            if drop_time <= pick_time:
                raise ValidationError(
                    "Drop-off time must be after pick-up time for same-day bookings"
                )

        # Maximum 90-day rental period
        days_diff = (drop_date - pick_date).days
        if days_diff > 90:
            raise ValidationError(
                "Maximum rental period is 90 days"
            )

        return data
