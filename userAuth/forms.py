from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class SignUpForm(forms.ModelForm):
    country_code = forms.CharField(max_length=6, required=True)
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
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()

        code = cleaned_data.get("country_code")
        phone = cleaned_data.get("phone_number")

        if not code or not phone:
            raise ValidationError("Phone number is required")

        phone = phone.replace(" ", "")

        if not phone.isdigit():
            raise ValidationError("Phone number must contain digits only")

        cleaned_data["phone_number"] = f"{code}{phone}"

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


class UserManageForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, required=False)
    is_verified = forms.BooleanField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "is_staff", "is_active", "is_superuser"]

    def __init__(self, *args, **kwargs):
        self.is_create = kwargs.pop("is_create", False)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            base_class = "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            if field.widget.__class__.__name__ in {"CheckboxInput"}:
                field.widget.attrs.update({"class": "h-4 w-4 text-blue-600"})
            else:
                field.widget.attrs.update({"class": base_class})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Email already registered.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if self.is_create and not p1:
            raise ValidationError("Password is required for new users.")

        if p1 or p2:
            if p1 != p2:
                raise ValidationError("Passwords do not match")
            if p1 and len(p1) < 8:
                raise ValidationError("Password must be at least 8 characters")

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get("email")

        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user
