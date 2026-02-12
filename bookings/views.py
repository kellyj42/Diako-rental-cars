from django.shortcuts import render, get_object_or_404, redirect
from cars.models import Car
from .forms import BookingForm
from datetime import date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Booking
from dashboard.decorators import admin_required

from .models import Booking
# =========================
# SELECT VEHICLE
# =========================

def selectedVehicle(request):
    if request.method == "POST":
        car_id = request.POST.get("car_id")
        request.session["selected_car_id"] = car_id
        return redirect("home:home")

    return redirect("home:home")

# =========================
# BOOKING FORM
# =========================

def booking_form_view(request):
    car_id = request.session.get("selected_car_id")

    if not car_id:
        return redirect("home:home")

    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.car = car
            booking.status = "draft"
            booking.save()

            return redirect(
                "bookings:booking_details",
                booking_id=booking.id
            )

    else:
        form = BookingForm(initial={"car_id": car.id})

    return render(request, "bookings/bookingform.html", {
        "form": form,
        "selected_car": car
    })



# =========================
# CANCEL SELECTED CAR
# =========================





def cancel_selected_car(request):
    if request.method == "POST":
        request.session.pop("selected_car_id", None)
        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)



# =========================
# BOOKING DETAILS PAGE
# =========================

def booking_details_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    return render(request, "bookings/booking_details.html", {
        "booking": booking,
        "car": booking.car
    })


def save_booking_draft(request):
    if request.method == "POST":
        request.session["booking_draft"] = request.POST.dict()
        request.session.set_expiry(900)  # 15 minutes
        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)

@login_required(login_url="userAuth:login")
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.status == "confirmed":
        return redirect("home:order_success")

    booking.user = request.user
    booking.status = "confirmed"
    booking.save()

    return redirect("home:order_success_detail", booking_id=booking.id)

@login_required
def booking_history_view(request):
    bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related("car")
        .order_by("-created_at")
    )

    return render(request, "bookings/booking_history.html", {
        "bookings": bookings
    })


@admin_required
def booking_manage_list_view(request):
    bookings = (
        Booking.objects
        .select_related("car", "user")
        .order_by("-created_at")
    )
    if hasattr(request.user, "profile"):
        request.user.profile.last_seen_bookings_at = timezone.now()
        request.user.profile.save(update_fields=["last_seen_bookings_at"])
    return render(request, "bookings/booking_manage_list.html", {"bookings": bookings})


@admin_required
def booking_update_status_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()

    return redirect("bookings:booking_manage_list")


@admin_required
def booking_delete_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        booking.delete()
        return redirect("bookings:booking_manage_list")

    return render(request, "bookings/booking_confirm_delete.html", {"booking": booking})