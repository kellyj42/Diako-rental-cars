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

    # ✅ FIX #20: Stronger email validation
    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        
        # Basic email format validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("Enter a valid email address")
        
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered.")
        
        return email

    # ✅ FIX #20: Validate names - prevent XSS, empty names
    def clean_first_name(self):
        """Validate first name"""
        name = (self.cleaned_data.get("first_name") or "").strip()
        
        if not name:
            raise ValidationError("First name is required")
        
        if len(name) < 2:
            raise ValidationError("First name too short (minimum 2 characters)")
        
        if len(name) > 50:
            raise ValidationError("First name too long (maximum 50 characters)")
        
        # Allow letters, spaces, hyphens, apostrophes
        if not re.match(r"^[A-Za-z\s\-\']+$", name):
            raise ValidationError("First name contains invalid characters")
        
        return name

    def clean_last_name(self):
        """Validate last name"""
        name = (self.cleaned_data.get("last_name") or "").strip()
        
        if not name:
            raise ValidationError("Last name is required")
        
        if len(name) < 2:
            raise ValidationError("Last name too short (minimum 2 characters)")
        
        if len(name) > 50:
            raise ValidationError("Last name too long (maximum 50 characters)")
        
        # Allow letters, spaces, hyphens, apostrophes
        if not re.match(r"^[A-Za-z\s\-\']+$", name):
            raise ValidationError("Last name contains invalid characters")
        
        return name

    # ✅ FIX #20: Better password validation
    def clean(self):
        cleaned_data = super().clean()

        code = cleaned_data.get("country_code")
        phone = cleaned_data.get("phone_number")

        if not code or not phone:
            raise ValidationError("Phone number is required")

        # ✅ FIX #20: Better phone validation - allow + and spaces
        # Remove spaces and validate format
        phone_clean = phone.replace(" ", "").replace("-", "")
        
        # Country code should be 1-3 digits
        if not re.match(r'^\+?\d{1,3}$', code):
            raise ValidationError("Invalid country code")

        if not re.match(r'^\d{7,15}$', phone_clean):
            raise ValidationError("Phone number must be 7-15 digits")

        cleaned_data["phone_number"] = f"{code}{phone_clean}"

        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password2")

        if p1 != p2:
            raise ValidationError("Passwords do not match")

        if p1:
            # ✅ FIX #20: Enforce password strength requirements
            if len(p1) < 8:
                raise ValidationError("Password must be at least 8 characters")
            
            # Check for complexity: at least one uppercase, one lowercase, one digit
            if not re.search(r'[A-Z]', p1):
                raise ValidationError("Password must contain at least one uppercase letter")
            
            if not re.search(r'[a-z]', p1):
                raise ValidationError("Password must contain at least one lowercase letter")
            
            if not re.search(r'\d', p1):
                raise ValidationError("Password must contain at least one digit")
            
            # Check for common weak passwords
            weak_passwords = ['password', '12345678', 'qwerty', 'admin', 'letmein', 'welcome']
            if p1.lower() in weak_passwords:
                raise ValidationError("This password is too common. Please choose a stronger password.")

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

    # ✅ FIX #20: Better email validation in user manage form
    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("Enter a valid email address")
        
        qs = User.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Email already registered.")
        return email

    # ✅ FIX #20: Validate names in manage form too
    def clean_first_name(self):
        """Validate first name"""
        name = (self.cleaned_data.get("first_name") or "").strip()
        
        if not name:
            raise ValidationError("First name is required")
        
        if len(name) < 2:
            raise ValidationError("First name too short")
        
        if len(name) > 50:
            raise ValidationError("First name too long")
        
        if not re.match(r"^[A-Za-z\s\-\']+$", name):
            raise ValidationError("First name contains invalid characters")
        
        return name

    def clean_last_name(self):
        """Validate last name"""
        name = (self.cleaned_data.get("last_name") or "").strip()
        
        if not name:
            raise ValidationError("Last name is required")
        
        if len(name) < 2:
            raise ValidationError("Last name too short")
        
        if len(name) > 50:
            raise ValidationError("Last name too long")
        
        if not re.match(r"^[A-Za-z\s\-\']+$", name):
            raise ValidationError("Last name contains invalid characters")
        
        return name

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if self.is_create and not p1:
            raise ValidationError("Password is required for new users.")

        if p1 or p2:
            if p1 != p2:
                raise ValidationError("Passwords do not match")
            
            if p1:
                # ✅ FIX #20: Password strength in manage form
                if len(p1) < 8:
                    raise ValidationError("Password must be at least 8 characters")
                
                if not re.search(r'[A-Z]', p1) or not re.search(r'[a-z]', p1) or not re.search(r'\d', p1):
                    raise ValidationError("Password must contain uppercase, lowercase, and digits")

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
