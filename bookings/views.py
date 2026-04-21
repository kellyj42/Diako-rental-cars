from django.shortcuts import render, get_object_or_404, redirect
from cars.models import Car, CarCategory
from .forms import BookingForm
from datetime import date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Booking
from dashboard.decorators import admin_required
from django.core.paginator import Paginator
from django.urls import reverse
from urllib.parse import urlencode
import logging

logger = logging.getLogger(__name__)


def _is_ajax_request(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def _serialize_form_errors(form):
    errors = []

    for field_errors in form.errors.values():
        errors.extend(field_errors)

    errors.extend(form.non_field_errors())
    return [str(error) for error in errors]


def _serialize_validation_error(error):
    if hasattr(error, "message_dict"):
        errors = []
        for field_errors in error.message_dict.values():
            errors.extend(field_errors)
        return [str(item) for item in errors]

    if hasattr(error, "messages"):
        return [str(item) for item in error.messages]

    return [str(error)]


def _get_guest_booking(request, booking_id):
    guest_booking_id = request.session.get("guest_booking_id")
    if guest_booking_id != booking_id:
        return None

    return Booking.objects.filter(
        id=booking_id,
        user__isnull=True,
        is_deleted=False,
    ).first()


def _requires_booking_terms(request):
    if request.user.is_authenticated:
        return not getattr(request.user.profile, "has_accepted_booking_terms", False)
    return not request.session.get("booking_terms_accepted", False)


def _mark_booking_terms_accepted(request):
    if request.user.is_authenticated:
        request.user.profile.mark_booking_terms_accepted()
        request.session["booking_terms_accepted"] = True
    else:
        request.session["booking_terms_accepted"] = True

# =========================
# SELECT VEHICLE
# =========================

@require_http_methods(["POST"])
def selectedVehicle(request):
    """Car selection with authentication and validation"""
    car_id = request.POST.get("car_id")
    
    # Validate car_id exists and is available
    try:
        car = Car.objects.get(id=car_id)
    except (Car.DoesNotExist, ValueError):
        messages.error(request, "Invalid car selected")
        return redirect("home:home")
    
    request.session["selected_car_id"] = car_id
    messages.success(request, f"{car.display_name} selected successfully.")
    return redirect("home:home")

# =========================
# BOOKING FORM
# =========================

def booking_form_view(request):
    """Create new booking"""
    car_id = request.session.get("selected_car_id")

    if not car_id:
        messages.error(request, "Please select a car first")
        return redirect("home:home")

    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        messages.error(request, "Selected car no longer available")
        return redirect("home:home")

    if request.method == "POST":
        guest_booking_id = request.session.get("guest_booking_id")
        existing_guest_booking = None
        if not request.user.is_authenticated and guest_booking_id:
            existing_guest_booking = Booking.objects.filter(
                id=guest_booking_id,
                user__isnull=True,
                status="draft",
                is_deleted=False,
            ).first()

        require_terms = False  # Terms accepted on confirm, not on draft creation
        form = BookingForm(request.POST, instance=existing_guest_booking, require_terms=require_terms)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.car = car
            booking.user = request.user if request.user.is_authenticated else None
            booking.driver_required = True
            booking.status = "draft"

            try:
                booking.save()
                if require_terms:
                    _mark_booking_terms_accepted(request)
                if request.user.is_authenticated:
                    request.session.pop("guest_booking_id", None)
                else:
                    request.session["guest_booking_id"] = booking.id
                messages.success(request, "Booking created! Redirecting to booking details...")
                actor = request.user.username if request.user.is_authenticated else "guest"
                logger.info(f"Booking created by {actor}: {booking.id}")
                if _is_ajax_request(request):
                    return JsonResponse({
                        "success": True,
                        "redirect_url": reverse("bookings:booking_details", kwargs={"booking_id": booking.id}),
                    })
                return redirect("bookings:booking_details", booking_id=booking.id)
            except ValidationError as e:
                logger.error(f"Booking validation error: {e}")
                errors = _serialize_validation_error(e)
                if errors:
                    form.add_error(None, errors[0])
                if _is_ajax_request(request):
                    return JsonResponse(
                        {"success": False, "errors": errors or ["Booking details are invalid."]},
                        status=400,
                    )
                for error_message in errors or ["Booking details are invalid."]:
                    messages.error(request, error_message)
            except Exception as e:
                logger.error(f"Booking creation error: {e}")
                if _is_ajax_request(request):
                    return JsonResponse(
                        {"success": False, "errors": ["Error creating booking. Please try again."]},
                        status=400,
                    )
                messages.error(request, "Error creating booking. Please try again.")
        else:
            # Clear direct form redirect behavior and explain problem
            if _is_ajax_request(request):
                return JsonResponse(
                    {
                        "success": False,
                        "errors": _serialize_form_errors(form),
                    },
                    status=400,
                )
            messages.error(request, "Please correct the highlighted booking form fields and submit again.")

    else:
        form = BookingForm(initial={"car_id": car.id}, require_terms=_requires_booking_terms(request))

    return render(request, "bookings/bookingform.html", {
        "form": form,
        "selected_car": car
    })

# =========================
# CANCEL SELECTED CAR
# =========================

@require_http_methods(["POST"])
def cancel_selected_car(request):
    """Cancel car selection"""
    if request.method == "POST":
        request.session.pop("selected_car_id", None)
        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)

# =========================
# BOOKING DETAILS PAGE
# =========================

def booking_details_view(request, booking_id):
    """View booking details for the signed-in user or current guest session."""
    booking = get_object_or_404(Booking, id=booking_id, is_deleted=False)

    if booking.user_id:
        if not request.user.is_authenticated:
            login_url = reverse("userAuth:login")
            return redirect(f"{login_url}?{urlencode({'next': request.get_full_path()})}")

        if booking.user != request.user and not request.user.is_staff:
            messages.error(request, "You do not have permission to view that booking.")
            return redirect("home:home")
    else:
        guest_booking = _get_guest_booking(request, booking.id)
        if not guest_booking and not (request.user.is_authenticated and request.user.is_staff):
            messages.error(request, "That guest booking session has expired. Please start again.")
            return redirect("home:home")

    total_price = booking.get_total_price()
    
    return render(request, "bookings/booking_details.html", {
        "booking": booking,
        "car": booking.car,
        "total_price": total_price,
        "require_terms": _requires_booking_terms(request),
    })

# ✅ FIX #4: Add @login_required to draft save
@require_http_methods(["POST"])
def save_booking_draft(request):
    """Save booking as draft"""
    selected_car_id = request.session.get("selected_car_id")
    
    if not selected_car_id:
        return JsonResponse({"success": False, "error": "No car selected"}, status=400)
    
    try:
        car = Car.objects.get(id=selected_car_id)
    except Car.DoesNotExist:
        return JsonResponse({"success": False, "error": "Car not found"}, status=400)
    
    existing_guest_booking = None
    guest_booking_id = request.session.get("guest_booking_id")
    if not request.user.is_authenticated and guest_booking_id:
        existing_guest_booking = Booking.objects.filter(
            id=guest_booking_id,
            user__isnull=True,
            status="draft",
            is_deleted=False,
        ).first()

    require_terms = _requires_booking_terms(request)
    form = BookingForm(request.POST, instance=existing_guest_booking, require_terms=require_terms)
    if form.is_valid():
        booking = form.save(commit=False)
        booking.car = car
        booking.user = request.user if request.user.is_authenticated else None
        booking.driver_required = True
        booking.status = "draft"
        
        try:
            booking.save()
            if require_terms:
                _mark_booking_terms_accepted(request)
            if request.user.is_authenticated:
                request.session.pop("guest_booking_id", None)
            else:
                request.session["guest_booking_id"] = booking.id
            request.session.set_expiry(900)  # 15 minutes
            logger.info(f"Draft booking saved: {booking.id}")
            return JsonResponse({"success": True, "booking_id": booking.id})
        except Exception as e:
            logger.error(f"Draft save error: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    
    return JsonResponse({"success": False, "error": "Form invalid"}, status=400)

# ✅ FIX #2, #25: Verify ownership + status transition validation
@login_required
def confirm_booking(request, booking_id):
    """Confirm booking - verify ownership and status"""
    booking = get_object_or_404(Booking, id=booking_id, is_deleted=False)

    if booking.user_id:
        if booking.user != request.user and not request.user.is_staff:
            messages.error(request, "You do not have permission to confirm that booking.")
            return redirect("home:home")
    else:
        guest_booking = _get_guest_booking(request, booking.id)
        if not guest_booking:
            messages.error(request, "That guest booking session has expired. Please start again.")
            return redirect("home:home")

    if request.method != "POST":
        messages.info(request, "Please use the confirm button to complete your booking.")
        return redirect("bookings:booking_details", booking_id=booking.id)

    # Check terms acceptance
    if _requires_booking_terms(request):
        if not request.POST.get('agree_terms'):
            messages.error(request, "Please accept the terms and conditions to confirm your booking.")
            return redirect("bookings:booking_details", booking_id=booking.id)
        _mark_booking_terms_accepted(request)

    if booking.status == "confirmed":
        messages.info(request, "This booking has already been confirmed.")
        return redirect("home:order_success_detail", booking_id=booking.id)

    if booking.status != "draft":
        messages.error(request, "Only draft bookings can be confirmed.")
        return redirect("bookings:booking_details", booking_id=booking.id)

    if booking.user_id is None:
        booking.user = request.user

    # ✅ FIX #25: Validate status transition
    if not booking.is_valid_status_transition("confirmed"):
        messages.error(request, "Invalid booking status for confirmation")
        return redirect("bookings:booking_details", booking_id=booking.id)

    booking.status = "confirmed"
    try:
        booking.save()
        request.session.pop("guest_booking_id", None)
        messages.success(request, "Booking confirmed successfully!")
        logger.info(f"Booking confirmed by {request.user.username}: {booking.id}")
    except Exception as e:
        logger.error(f"Booking confirmation error: {e}")
        messages.error(request, "Error confirming booking")

    return redirect("home:order_success_detail", booking_id=booking.id)

# ✅ FIX #13: Add pagination
@login_required
def booking_history_view(request):
    """View user's booking history with pagination"""
    bookings = (
        Booking.objects
        .filter(user=request.user, is_deleted=False)
        .select_related("car")
        .order_by("-created_at")
    )

    # ✅ FIX #13: Pagination
    paginator = Paginator(bookings, 10)  # 10 per page
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    total_bookings = bookings.count()
    upcoming_bookings = bookings.filter(status__in=["draft", "confirmed"]).count()
    completed_bookings = bookings.filter(status="completed").count()
    cancelled_bookings = bookings.filter(status="cancelled").count()

    popular_categories = CarCategory.objects.filter().order_by('-id')[:4]

    return render(request, "bookings/booking_history.html", {
        "page_obj": page_obj,
        "bookings": page_obj.object_list,
        "total_bookings": total_bookings,
        "upcoming_bookings": upcoming_bookings,
        "completed_bookings": completed_bookings,
        "cancelled_bookings": cancelled_bookings,
        "popular_categories": popular_categories,
    })

@admin_required
def booking_manage_list_view(request):
    """Admin: Manage all bookings with pagination"""
    bookings = (
        Booking.objects
        .filter(is_deleted=False)
        .select_related("car", "user")
        .order_by("-created_at")
    )
    
    # Filter by status if provided
    status = request.GET.get("status")
    if status in dict(Booking.STATUS_CHOICES):
        bookings = bookings.filter(status=status)
    
    # ✅ FIX #13: Pagination
    paginator = Paginator(bookings, 20)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    if hasattr(request.user, "profile"):
        request.user.profile.last_seen_bookings_at = timezone.now()
        request.user.profile.save(update_fields=["last_seen_bookings_at"])
    
    return render(request, "bookings/booking_manage_list.html", {
        "page_obj": page_obj,
        "bookings": page_obj.object_list,
        "statuses": Booking.STATUS_CHOICES,
    })

@login_required
@require_http_methods(["POST"])
def cancel_booking_view(request, booking_id):
    """Allow user to cancel own draft/confirmed booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, is_deleted=False)

    if booking.status not in ["draft", "confirmed"]:
        messages.error(request, "Only pending bookings can be canceled.")
        return redirect("bookings:booking_history")

    booking.status = "cancelled"
    booking.save(update_fields=["status", "updated_at"])
    messages.success(request, f"Booking #{booking.id} canceled successfully.")
    return redirect("bookings:booking_history")

@admin_required
@require_http_methods(["POST"])
def booking_update_status_view(request, booking_id):
    """Admin: Update booking status with validation"""
    booking = get_object_or_404(Booking, id=booking_id, is_deleted=False)

    new_status = request.POST.get("status")
    
    # ✅ FIX #25: Validate status transition
    if new_status in dict(Booking.STATUS_CHOICES):
        if booking.is_valid_status_transition(new_status):
            booking.status = new_status
            try:
                booking.save()
                messages.success(request, f"Booking status updated to {new_status}")
                logger.info(f"Booking {booking_id} status changed to {new_status} by {request.user.username}")
            except Exception as e:
                logger.error(f"Status update error: {e}")
                messages.error(request, "Error updating status")
        else:
            messages.error(request, f"Cannot transition from {booking.status} to {new_status}")
    else:
        messages.error(request, "Invalid status")

    return redirect("bookings:booking_manage_list")

@admin_required
@require_http_methods(["GET", "POST"])
def booking_delete_view(request, booking_id):
    """Admin: Delete booking (soft delete)"""
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        try:
            booking.soft_delete()  # ✅ FIX #20: Use soft delete
            messages.success(request, "Booking deleted")
            logger.info(f"Booking {booking_id} soft-deleted by {request.user.username}")
            return redirect("bookings:booking_manage_list")
        except Exception as e:
            logger.error(f"Booking deletion error: {e}")
            messages.error(request, "Error deleting booking")

    return render(request, "bookings/booking_confirm_delete.html", {"booking": booking})


@admin_required
@require_http_methods(["POST"])
def booking_bulk_delete_view(request):
    """Admin: Bulk soft delete bookings."""
    booking_ids = request.POST.getlist("selected_ids")

    if not booking_ids:
        messages.error(request, "Select at least one booking to delete.")
        return redirect("bookings:booking_manage_list")

    deleted_count = 0
    failed_count = 0

    for booking in Booking.objects.filter(id__in=booking_ids, is_deleted=False):
        try:
            booking.soft_delete()
            deleted_count += 1
        except Exception:
            failed_count += 1

    if deleted_count:
        messages.success(request, f"{deleted_count} booking(s) deleted successfully.")
    if failed_count:
        messages.error(request, f"{failed_count} booking(s) could not be deleted.")

    return redirect("bookings:booking_manage_list")
