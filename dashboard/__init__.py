from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from bookings.models import Booking
from cars.models import Car
from userAuth.models import Profile
from .decorators import admin_required


@admin_required
def dashboard_home(request):
    today = timezone.localdate()
    seven_days_ago = today - timedelta(days=6)

    all_bookings = Booking.objects.filter(is_deleted=False)
    confirmed_bookings_qs = all_bookings.filter(status="confirmed")
    completed_bookings = all_bookings.filter(status="completed").count()
    cancelled_bookings = all_bookings.filter(status="cancelled").count()

    # Total revenue from confirmed and completed bookings
    booking_totals = [b.get_total_price() for b in all_bookings if b.status in ["confirmed", "completed"]]
    total_revenue = sum(booking_totals)

    avg_booking_value = Decimal("0")
    if all_bookings.count() > 0:
        avg_booking_value = total_revenue / Decimal(all_bookings.count())

    # Revenue by last 7 days for chart
    revenue_by_day = []
    for i in range(6, -1, -1):
        target_date = today - timedelta(days=i)
        day_revenue = sum(
            b.get_total_price()
            for b in all_bookings
            if b.status in ["confirmed", "completed"] and b.pick_up_date == target_date
        )
        revenue_by_day.append({
            "day": target_date.strftime("%a"),
            "revenue": day_revenue,
        })

    max_revenue = max([d["revenue"] for d in revenue_by_day] + [1])
    for item in revenue_by_day:
        item["percentage"] = int((item["revenue"] / max_revenue) * 100) if max_revenue > 0 else 0

    recent_bookings = all_bookings.select_related("car", "user").order_by("-created_at")[:5]
    todays_rentals = confirmed_bookings_qs.filter(pick_up_date=today).count()

    total_users = Profile.objects.count()
    verified_users = Profile.objects.filter(is_verified=True).count()
    customer_satisfaction = 4.8
    if total_bookings := all_bookings.count():
        fulfillment_rate = (confirmed_bookings_qs.count() / float(total_bookings)) * 100
        customer_satisfaction = round(3.8 + (fulfillment_rate / 100) * 1.2, 1)
        customer_satisfaction = min(max(customer_satisfaction, 3.2), 4.9)

    full_stars = int(customer_satisfaction)
    half_star = 1 if (customer_satisfaction - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    customer_star_display = "â˜…" * full_stars + ("Â½" if half_star else "") + "â˜†" * empty_stars

    context = {
        "total_bookings": all_bookings.count(),
        "pending_bookings": all_bookings.filter(status="draft").count(),
        "confirmed_bookings": confirmed_bookings_qs.count(),
        "completed_bookings": completed_bookings,
        "cancelled_bookings": cancelled_bookings,
        "total_cars": Car.objects.count(),
        "dashboard_version": "2.2",
        "footer_updated": timezone.now(),
        "footer_support_email": "support@diakorentals.com",
        "available_cars": Car.objects.filter(is_available=True).count(),
        "unverified_users": Profile.objects.filter(is_verified=False).count(),
        "total_revenue": total_revenue,
        "avg_booking_value": avg_booking_value,
        "todays_rentals": todays_rentals,
        "customer_satisfaction": customer_satisfaction,
        "customer_star_display": customer_star_display,
        "revenue_by_day": revenue_by_day,
        "recent_bookings": recent_bookings,
        "cars_inventory": Car.objects.order_by("name")[:8],
        "bookings_list": all_bookings.order_by("-created_at")[:10],
    }

    return render(request, "dashboard/index.html", context)
