from django.shortcuts import render

# Create your views here.
# dashboard/views.py
from django.shortcuts import render
from bookings.models import Booking
from cars.models import Car
from userAuth.models import Profile
from .decorators import admin_required

@admin_required
def dashboard_home(request):
    context = {
        "total_bookings": Booking.objects.count(),
        "pending_bookings": Booking.objects.filter(status="pending").count(),
        "confirmed_bookings": Booking.objects.filter(status="confirmed").count(),
        "total_cars": Car.objects.count(),
        "available_cars": Car.objects.filter(is_available=True).count(),
        "unverified_users": Profile.objects.filter(is_verified=False).count(),
    }
    return render(request, "dashboard/index.html", context)
