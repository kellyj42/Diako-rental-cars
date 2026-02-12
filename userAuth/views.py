from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from userAuth.tokens import email_verification_token
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, url_has_allowed_host_and_scheme
from django.urls import reverse
from urllib.parse import urlencode
from .forms import SignUpForm, UserManageForm
from .models import Profile
from .utils import send_verification_email
from dashboard.decorators import admin_required


# Create your views here.

def login_view(request):
    next_url = request.POST.get("next") or request.GET.get("next") or request.session.get("auth_next")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        request.session["auth_next"] = next_url

    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user:
            if not user.profile.is_verified:
                messages.warning(request, "Please verify your email before logging in.")
                # send_verification_email(request, user)
                return redirect("userAuth:email_verification")
            
            if user.is_staff:
                login(request, user)
                return redirect("dashboard:home")
            
            login(request, user)
            redirect_to = request.session.pop("auth_next", None)
            if redirect_to and url_has_allowed_host_and_scheme(redirect_to, allowed_hosts={request.get_host()}):
                return redirect(redirect_to)
            return redirect("home:home")

        messages.error(request, "Invalid email or password.")

    return render(request, "userAuth/login.html", {"next": next_url})

from .utils import send_verification_email

def signup_view(request):
    next_url = request.POST.get("next") or request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        request.session["auth_next"] = next_url

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            profile = user.profile
            profile.phone_number = form.cleaned_data.get("phone_number", "")
            profile.save()
            request.session["verify_user_id"] = user.id
            request.session["verify_email"] = user.email
            # send_verification_email(request, user)
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
    next_url = request.session.get("auth_next")
    return render(request, "userAuth/emailVerification.html", {"email": email, "next": next_url})


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
            messages.info(request, "Your email is already verified. You can now enter your login details")
            next_url = request.session.get("auth_next")
            login_url = reverse("userAuth:login")
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(f"{login_url}?{urlencode({'next': next_url})}")
            return redirect("userAuth:login")

        profile.is_verified = True
        profile.save()

        messages.success(request, "Your email has been verified successfully.")
        next_url = request.session.get("auth_next")
        login_url = reverse("userAuth:login")
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(f"{login_url}?{urlencode({'next': next_url})}")
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


@admin_required
def user_manage_list_view(request):
    users = User.objects.select_related("profile").all().order_by("-date_joined")
    return render(request, "userAuth/user_manage_list.html", {"users": users})


@admin_required
def user_create_view(request):
    if request.method == "POST":
        form = UserManageForm(request.POST, is_create=True)
        if form.is_valid():
            user = form.save()
            profile = user.profile
            profile.phone_number = form.cleaned_data.get("phone_number") or ""
            profile.is_verified = form.cleaned_data.get("is_verified", False)
            profile.save()
            return redirect("userAuth:user_manage_list")
    else:
        form = UserManageForm(is_create=True)

    return render(request, "userAuth/user_form.html", {"form": form, "mode": "create"})


@admin_required
def user_update_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    initial = {
        "phone_number": getattr(user.profile, "phone_number", ""),
        "is_verified": getattr(user.profile, "is_verified", False),
    }

    if request.method == "POST":
        form = UserManageForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            profile = user.profile
            profile.phone_number = form.cleaned_data.get("phone_number") or ""
            profile.is_verified = form.cleaned_data.get("is_verified", False)
            profile.save()
            return redirect("userAuth:user_manage_list")
    else:
        form = UserManageForm(instance=user, initial=initial)

    return render(request, "userAuth/user_form.html", {"form": form, "mode": "update", "user_obj": user})


@admin_required
def user_delete_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect("userAuth:user_manage_list")

    if request.method == "POST":
        user.delete()
        return redirect("userAuth:user_manage_list")

    return render(request, "userAuth/user_confirm_delete.html", {"user_obj": user})
