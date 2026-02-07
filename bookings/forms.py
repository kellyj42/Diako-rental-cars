from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
import re
from .models import Booking


TEXT_PATTERN = re.compile(r"^[A-Za-z\s\-.,']+$")


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
            "additional_notes",

        ]

    agree_terms = forms.BooleanField(required=True)

    # -------------------------
    # LOCATION VALIDATION
    # -------------------------

    def clean_pick_up_location(self):
        value = self.cleaned_data["pick_up_location"].strip()

        if not TEXT_PATTERN.match(value):
            raise ValidationError(
                "Pickup location must contain letters only."
            )

        if len(value) < 3:
            raise ValidationError("Pickup location too short.")

        return value


    def clean_drop_off_location(self):
        value = self.cleaned_data["drop_off_location"].strip()

        if not TEXT_PATTERN.match(value):
            raise ValidationError(
                "Dropoff location must contain letters only."
            )

        if len(value) < 3:
            raise ValidationError("Dropoff location too short.")

        return value


    # -------------------------
    # TEXTAREA SECURITY
    # -------------------------

    def clean_additional_notes(self):
        text = self.cleaned_data.get("additional_notes", "").strip()

        if not text:
            return text

        # block HTML tags
        if "<" in text or ">" in text:
            raise ValidationError("HTML is not allowed.")

        # block script patterns
        blocked_words = [
            "script",
            "iframe",
            "javascript",
            "onload",
            "onerror"
        ]

        lower = text.lower()
        for word in blocked_words:
            if word in lower:
                raise ValidationError("Suspicious content detected.")

        # spam character flood
        if re.search(r"(.)\1{20,}", text):
            raise ValidationError("Spam pattern detected.")

        # non printable chars
        if not text.isprintable():
            raise ValidationError("Invalid characters detected.")

        return text


    # -------------------------
    # DATE LOGIC VALIDATION
    # -------------------------

    def clean(self):
        data = super().clean()

        pick_date = data.get("pick_up_date")
        drop_date = data.get("drop_off_date")

        if not pick_date or not drop_date:
            return data

        today = timezone.now().date()

        if pick_date < today:
            raise ValidationError(
                "Pickup date cannot be in the past."
            )

        if drop_date < pick_date:
            raise ValidationError(
                "Dropoff date must be after pickup date."
            )

        if (drop_date - pick_date).days > 60:
            raise ValidationError(
                "Rental period too long."
            )

        return data
