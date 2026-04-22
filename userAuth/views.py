from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from userAuth.tokens import email_verification_token
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, url_has_allowed_host_and_scheme
from django.urls import reverse
from urllib.parse import urlencode
from django.views.decorators.http import require_http_methods
from .forms import SignUpForm, UserManageForm
from .models import Profile
from .utils import send_verification_email
from dashboard.decorators import admin_required
from bookings.models import Booking


# Create your views here.
AUTH_MESSAGE_TAG = "auth"


def _is_user_verified(user):
    profile = user.profile
    if profile.is_verified:
        return True

    has_verified_email = EmailAddress.objects.filter(user=user, verified=True).exists()
    has_social_account = user.socialaccount_set.exists()
    if has_verified_email or has_social_account:
        profile.is_verified = True
        profile.save(update_fields=["is_verified"])
        return True

    return False


def login_view(request):
    next_url = request.POST.get("next") or request.GET.get("next") or request.session.get("auth_next")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        request.session["auth_next"] = next_url

    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me") == "on"

        user = authenticate(request, username=email, password=password)

        if user:
            if not _is_user_verified(user):
                messages.warning(request, "Please verify your email before logging in.", extra_tags=AUTH_MESSAGE_TAG)
                email_sent = send_verification_email(request, user)
                if not email_sent:
                    messages.info(
                        request,
                        "We could not send the verification email right now. Please try again later or contact support.",
                        extra_tags=AUTH_MESSAGE_TAG,
                    )
                return redirect("userAuth:email_verification")
            
            if user.is_staff:
                login(request, user)
                request.session.set_expiry(60 * 60 * 24 * 30 if remember_me else 0)
                return redirect("dashboard:home")
            
            login(request, user)
            request.session.set_expiry(60 * 60 * 24 * 30 if remember_me else 0)
            redirect_to = request.session.pop("auth_next", None)
            if redirect_to and url_has_allowed_host_and_scheme(redirect_to, allowed_hosts={request.get_host()}):
                return redirect(redirect_to)
            return redirect("home:home")

        messages.error(request, "Invalid email or password.", extra_tags=AUTH_MESSAGE_TAG)

    return render(request, "userAuth/login.html", {"next": next_url})

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
            email_sent = send_verification_email(request, user)
            if email_sent:
                messages.success(
                    request,
                    "Account created. We have sent a verification email to continue.",
                    extra_tags=AUTH_MESSAGE_TAG,
                )
            else:
                messages.warning(
                    request,
                    "Account created, but we could not send the verification email right now. You can try resending it from the verification page.",
                    extra_tags=AUTH_MESSAGE_TAG,
                )
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
        messages.error(request, "Invalid verification link.", extra_tags=AUTH_MESSAGE_TAG)
        return redirect("userAuth:email_verification")

    if email_verification_token.check_token(user, token):
        profile = user.profile

        if _is_user_verified(user):
            request.session.pop("verify_user_id", None)
            request.session.pop("verify_email", None)
            messages.info(
                request,
                "Your email is already verified. You can now enter your login details",
                extra_tags=AUTH_MESSAGE_TAG,
            )
            next_url = request.session.get("auth_next")
            login_url = reverse("userAuth:login")
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(f"{login_url}?{urlencode({'next': next_url})}")
            return redirect("userAuth:login")

        profile.is_verified = True
        profile.save(update_fields=["is_verified"])
        request.session.pop("verify_user_id", None)
        request.session.pop("verify_email", None)

        messages.success(request, "Your email has been verified successfully.", extra_tags=AUTH_MESSAGE_TAG)
        next_url = request.session.get("auth_next")
        login_url = reverse("userAuth:login")
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(f"{login_url}?{urlencode({'next': next_url})}")
        return redirect("userAuth:login")

    messages.error(request, "Verification link is invalid or has expired.", extra_tags=AUTH_MESSAGE_TAG)
    return redirect("userAuth:email_verification")


@require_http_methods(["POST"])
def resend_verification_email(request):
    user = None

    if request.user.is_authenticated:
        user = request.user
    else:
        verify_user_id = request.session.get("verify_user_id")
        if verify_user_id:
            user = User.objects.filter(pk=verify_user_id).first()

    if not user:
        messages.error(
            request,
            "Your verification session has expired. Please sign up or log in again.",
            extra_tags=AUTH_MESSAGE_TAG,
        )
        return redirect("userAuth:login")

    if _is_user_verified(user):
        request.session.pop("verify_user_id", None)
        request.session.pop("verify_email", None)
        return redirect("home:home")

    request.session["verify_user_id"] = user.id
    request.session["verify_email"] = user.email
    email_sent = send_verification_email(request, user)
    if email_sent:
        messages.success(request, "Verification email resent.", extra_tags=AUTH_MESSAGE_TAG)
    else:
        messages.error(
            request,
            "We could not resend the verification email right now. Please try again later.",
            extra_tags=AUTH_MESSAGE_TAG,
        )
    return redirect("userAuth:email_verification")

def password_reset_link(request):

    return render(request, 'userAuth/_passwordLink.html')

@login_required
def profile_view(request):
    bookings = (
        Booking.objects
        .filter(user=request.user, is_deleted=False)
        .select_related("car")
        .order_by("-created_at")
    )

    total_bookings = bookings.count()
    completed_bookings = bookings.filter(status="completed").count()
    upcoming_bookings = bookings.filter(status__in=["draft", "confirmed"]).count()
    total_spent = sum(
        booking.get_total_price()
        for booking in bookings.filter(status__in=["confirmed", "completed"])
    )

    return render(
        request,
        "userAuth/profile.html",
        {
            "bookings": bookings[:3],
            "total_bookings": total_bookings,
            "completed_bookings": completed_bookings,
            "upcoming_bookings": upcoming_bookings,
            "total_spent": total_spent,
        },
    )


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


@admin_required
@require_http_methods(["POST"])
def user_bulk_delete_view(request):
    user_ids = request.POST.getlist("selected_ids")

    if not user_ids:
        messages.error(request, "Select at least one user to delete.")
        return redirect("userAuth:user_manage_list")

    deleted_count = 0
    skipped_count = 0

    for user in User.objects.filter(id__in=user_ids):
        if user == request.user:
            skipped_count += 1
            continue
        user.delete()
        deleted_count += 1

    if deleted_count:
        messages.success(request, f"{deleted_count} user(s) deleted successfully.")
    if skipped_count:
        messages.error(request, "Your own account was skipped and not deleted.")

    return redirect("userAuth:user_manage_list")
