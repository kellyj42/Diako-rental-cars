from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from cars.models import Car
from bookings.models import Booking
from content.content import services,achievements,vehicles,nav_links


def indexView(request):
    selected_car = None
    selected_car_id = request.session.get('selected_car_id')

    if selected_car_id:
        try:
            selected_car = Car.objects.get(id=selected_car_id)
        except Car.DoesNotExist:
            selected_car = None

    return render(request, 'home/homepage.html',
                {
                 "services": services,
                 "achievements": achievements,
                 "vehicles": vehicles,
                 "nav_links": nav_links,
                 "selected_car": selected_car,
                })

def bookingDetailsView(request):
    return render(request, 'home/booking_details.html')

@login_required
def orderSuccessView(request, booking_id=None):
    if not booking_id:
        return redirect("home:home")

    if request.user.is_staff:
        booking = get_object_or_404(Booking, id=booking_id)
    else:
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status != "confirmed" and not request.user.is_staff:
        return redirect("bookings:booking_details", booking_id=booking.id)

    rental_days = (booking.drop_off_date - booking.pick_up_date).days
    rental_days = rental_days if rental_days > 0 else 1

    daily_rate = booking.car.price_per_day or 0
    estimate_total = daily_rate * rental_days
    phone = ""
    if hasattr(booking.user, "profile"):
        phone = booking.user.profile.phone_number

    context = {
        "booking": booking,
        "phone": phone,
        "car": booking.car,
        "rental_days": rental_days,
        "daily_rate": daily_rate,
        "estimate_total": estimate_total,
        "booking_reference": f"DRC-{booking.id:06d}",
    }

    return render(request, "home/order_success.html", context)

def about_us_view(request):
    return render(request, 'home/aboutpage.html',{
                    "nav_links": nav_links
             })
def services_view(request):
    return render(request, 'home/servicespage.html',
                 {
                    "services": services, 
                    "nav_links": nav_links
             })

def our_story_view(request):
    return render(request, 'home/our_story.html', {
        "nav_links": nav_links,
    })

def team_view(request):
    return render(request, 'home/team.html', {
        "nav_links": nav_links,
    })

def careers_view(request):
    return render(request, 'home/careers.html', {
        "nav_links": nav_links,
    })

def faqs_view(request):
    return render(request, 'home/faqs.html', {
        "nav_links": nav_links,
    })

def contact_view(request):
    return render(request, 'home/contact.html', {
        "nav_links": nav_links,
    })
