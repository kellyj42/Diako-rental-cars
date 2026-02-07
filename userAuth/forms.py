from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class SignUpForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15,
        required=True
    )

    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered.")
        return email

    def clean(self):
        cleaned = super().clean()

        code = cleaned.get("country_code")
        phone = cleaned.get("phone_number")

        if not code or not phone:
            raise ValidationError("Phone number is required")

    # Remove spaces
        phone = phone.replace(" ", "")

    # Digits only
        if not phone.isdigit():
            raise ValidationError("Phone number must contain digits only")

        cleaned["phone_number"] = f"{code}{phone}"
        return cleaned

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password2")

        if p1 != p2:
            raise ValidationError("Passwords do not match")

        if p1 and len(p1) < 8:
            raise ValidationError("Password must be at least 8 characters")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # username required by Django
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user
