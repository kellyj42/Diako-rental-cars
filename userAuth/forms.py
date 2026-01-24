# from django import forms
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError


# class SignUpForm(forms.ModelForm):
#     phone_number = forms.CharField(
#         max_length=15,
#         required=True,
#         widget=forms.TextInput(attrs={
#             "placeholder": "e.g. +256701234567"
#         })
#     )
    
#     password = forms.CharField(
#         label="Password",
#         widget=forms.PasswordInput(attrs={
#             "class": "w-full px-4 py-3 border rounded-xl",
#             "placeholder": "Enter password"
#         })
#     )

#     password2 = forms.CharField(
#         label="Confirm Password",
#         widget=forms.PasswordInput(attrs={
#             "class": "w-full px-4 py-3 border rounded-xl",
#             "placeholder": "Confirm password"
#         })
#     )

#     class Meta:
#         model = User
#         fields = ["first_name", "last_name", "email"]
#         widgets = {
#             "first_name": forms.TextInput(attrs={
#                 "class": "w-full px-4 py-3 border rounded-xl",
#                 "placeholder": "First Name"
#             }),
#               "last_name": forms.TextInput(attrs={
#                 "class": "w-full px-4 py-3 border rounded-xl",
#                 "placeholder": "Last Name"
#             }),
#             "email": forms.EmailInput(attrs={
#                 "class": "w-full px-4 py-3 border rounded-xl",
#                 "placeholder": "Email address"
#             }),
#         }

#     # 🔍 FILTER 1: Unique Email
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         if User.objects.filter(email=email).exists():
#             raise ValidationError("Email already registered.")
#         return email

#     # 🔍 FILTER 2: Unique Username
#     def clean_username(self):
#         username = self.cleaned_data.get("first_name") + self.cleaned_data.get("last_name")
#         if User.objects.filter(username=username).exists():
#             raise ValidationError("Username already taken.")
#         return username

#     # 🔍 FILTER 2: Unique contact
#     def clean_phone_number(self):
#         phone = self.cleaned_data.get("phone")

#         # Uganda example (+256)
#         pattern = r"^\+2567\d{8}$"

#         if not re.match(pattern, phone):
#             raise ValidationError(
#                 "Enter a valid phone number (e.g. +2567XXXXXXXX)"
#             )

#     # 🔍 FILTER 3: Password match
#     def clean(self):
#         cleaned_data = super().clean()
#         p1 = cleaned_data.get("password")
#         p2 = cleaned_data.get("confirm_password")

#         if p1 and p2 and p1 != p2:
#             raise ValidationError("Passwords do not match.")

#         if p1 and len(p1) < 8:
#             raise ValidationError("Password must be at least 8 characters.")

#         return cleaned_data
