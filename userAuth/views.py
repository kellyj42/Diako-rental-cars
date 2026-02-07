from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from userAuth.tokens import email_verification_token
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .forms import SignUpForm
from .models import Profile
from .utils import send_verification_email


# Create your views here.

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user:
            if not user.profile.is_verified:
                messages.warning(request, "Please verify your email before logging in.")
                send_verification_email(request, user)
                return redirect("userAuth:email_verification")
            
            if user.is_staff:
                return redirect("dashboard:home")
            
            login(request, user)
            return redirect("home:home")

        messages.error(request, "Invalid email or password.")

    return render(request, "userAuth/login.html")

from .utils import send_verification_email

def signup_view(request):
    next_url = request.POST.get("next") or request.GET.get("next")

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            request.session["verify_user_id"] = user.id
            request.session["verify_email"] = user.email
            send_verification_email(request, user)
            return redirect("userAuth:email_verification")  

    else:
        form = SignUpForm()

    return render(
        request,
        "userAuth/signUp.html",
        {"form": form, "next": next_url}
    )



def reset_password_view(request):
    return render(request, 'userAuth/resetpassword.html')


def email_verification_view(request):
    email = request.session.get("verify_email")
    return render(request, "userAuth/emailVerification.html", {"email": email})


def logout_view(request):
    logout(request)
    return redirect("home:home")



def verify_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if not user:
        print("VERIFY: user not found")
        messages.error(request, "Invalid verification link.")
        return redirect("userAuth:email_verification")

    token = email_verification_token.make_token(user)
    print("VERIFY TOKEN RESULT:", token)

    if token:
        profile = user.profile

        if profile.is_verified:
            messages.info(request, "Your email is already verified.")
            return redirect("userAuth:login")

        profile.is_verified = True
        profile.save()

        messages.success(request, "Your email has been verified successfully.")
        return redirect("userAuth:login")

    messages.error(request, "Verification link is invalid or has expired.")
    return redirect("userAuth:email_verification")



def resend_verification_email(request):
    if request.user.profile.is_verified:
        return redirect("home:home")

    send_verification_email(request, request.user)
    messages.success(request, "Verification email resent.")
    return redirect("userAuth:email_verification")

def password_reset_link(request):

    return render(request, 'userAuth/_passwordLink.html')

@login_required
def profile_view(request):
    return render(request, "userAuth/profile.html")
