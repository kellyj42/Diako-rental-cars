from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.contrib import messages
# from .forms import SignUpForm

# Create your views here.

def login_view(request):
    return render(request, "userAuth/login.html")
def signup_view(request):
    return render(request, "userAuth/signUp.html", )
def reset_password_view(request):
    return render(request, 'userAuth/resetpassword.html')
def email_verification_view(request):
    return render(request, 'userAuth/emailVerification.html')
def logout_view(request):
    return render(request, 'userAuth/logout.html')