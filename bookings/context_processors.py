from django.utils import timezone
from .models import Booking


def pending_bookings_count(request):
    if request.user.is_authenticated and request.user.is_staff:
        last_seen = getattr(request.user.profile, "last_seen_bookings_at", None)
        qs = Booking.objects.filter(status="draft")
        if last_seen:
            qs = qs.filter(created_at__gt=last_seen)
        return {
            "pending_bookings": qs.count()
        }
    return {"pending_bookings": 0}
