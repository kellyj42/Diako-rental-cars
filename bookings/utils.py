import logging

import resend
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import escape

from content.content import contact_info

logger = logging.getLogger(__name__)


def _absolute_url(request, path):
    if settings.APP_BASE_URL:
        return f"{settings.APP_BASE_URL.rstrip('/')}{path}"
    return request.build_absolute_uri(path)


def get_booking_notification_recipients():
    if settings.BOOKING_NOTIFICATION_EMAILS:
        return settings.BOOKING_NOTIFICATION_EMAILS

    User = get_user_model()
    superuser_emails = list(
        User.objects.filter(is_active=True, is_superuser=True)
        .exclude(email="")
        .values_list("email", flat=True)
    )
    if superuser_emails:
        return superuser_emails

    return [contact_info["email"]["support"]]


def send_booking_notification_email(request, booking):
    recipients = get_booking_notification_recipients()
    dashboard_url = _absolute_url(request, reverse("bookings:booking_manage_list"))
    admin_url = _absolute_url(request, reverse("admin:bookings_booking_change", args=[booking.id]))
    customer_name = booking.user.get_full_name() or booking.user.email if booking.user_id else "Guest"
    customer_email = booking.user.email if booking.user_id else "Guest booking"

    html_content = f"""
        <div style="background-color:#f5f7fb;padding:32px 0;font-family:Arial,sans-serif;">
            <div style="max-width:640px;margin:0 auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 10px 30px rgba(15,23,42,0.08);">
                <div style="background:#1e3a8a;padding:18px 24px;">
                    <h1 style="margin:0;color:#ffffff;font-size:20px;">New booking confirmed</h1>
                </div>
                <div style="padding:28px 32px;color:#0f172a;">
                    <p style="margin:0 0 16px;color:#475569;">A customer has confirmed a booking on Daiko Travel Agency Ltd.</p>
                    <table style="width:100%;border-collapse:collapse;font-size:14px;">
                        <tr><td style="padding:8px 0;color:#64748b;">Booking ID</td><td style="padding:8px 0;font-weight:700;">#{booking.id:06d}</td></tr>
                        <tr><td style="padding:8px 0;color:#64748b;">Customer</td><td style="padding:8px 0;">{escape(customer_name)} ({escape(customer_email)})</td></tr>
                        <tr><td style="padding:8px 0;color:#64748b;">Vehicle</td><td style="padding:8px 0;">{escape(booking.car.display_name)}</td></tr>
                        <tr><td style="padding:8px 0;color:#64748b;">Pick-up</td><td style="padding:8px 0;">{escape(booking.pick_up_location)} on {booking.pick_up_date} at {booking.pick_up_time}</td></tr>
                        <tr><td style="padding:8px 0;color:#64748b;">Drop-off</td><td style="padding:8px 0;">{escape(booking.drop_off_location)} on {booking.drop_off_date} at {booking.drop_off_time}</td></tr>
                        <tr><td style="padding:8px 0;color:#64748b;">Total</td><td style="padding:8px 0;font-weight:700;">UGX {booking.total_price}</td></tr>
                    </table>
                    <div style="margin:26px 0 8px;">
                        <a href="{dashboard_url}" style="display:inline-block;background:#f97316;color:#ffffff;text-decoration:none;padding:12px 20px;border-radius:999px;font-weight:700;">Open dashboard</a>
                    </div>
                    <p style="margin:12px 0 0;color:#64748b;font-size:13px;">Admin detail link: <a href="{admin_url}" style="color:#2563eb;">{admin_url}</a></p>
                </div>
            </div>
        </div>
    """

    if not settings.RESEND_API_KEY:
        logger.warning(
            "RESEND_API_KEY is not configured. Booking notification not sent for booking %s.",
            booking.id,
        )
        return False

    try:
        resend.api_key = settings.RESEND_API_KEY
        resend.Emails.send(
            {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": recipients,
                "subject": f"New booking confirmed #{booking.id:06d}",
                "html": html_content,
            }
        )
        return True
    except Exception:
        logger.exception("Failed to send booking notification for booking %s.", booking.id)
        return False
