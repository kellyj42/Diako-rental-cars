from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from bookings.models import Booking
from bookings.utils import get_booking_notification_recipients
from cars.models import Car, CarCategory


TEST_STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


@override_settings(STORAGES=TEST_STORAGES, RESEND_API_KEY="")
class GuestBookingFlowTests(TestCase):
    def setUp(self):
        self.category = CarCategory.objects.create(name="SUV")
        self.car = Car.objects.create(
            name="Toyota",
            model="Prado",
            year=2024,
            category=self.category,
            price_per_day=120,
            seats=5,
        )
        self.booking_payload = {
            "pick_up_location": "Airport Road",
            "drop_off_location": "City Center",
            "pick_up_date": (timezone.now().date() + timedelta(days=2)).isoformat(),
            "pick_up_time": "09:00",
            "drop_off_date": (timezone.now().date() + timedelta(days=4)).isoformat(),
            "drop_off_time": "10:00",
            "additional_notes": "Guest checkout flow",
            "agree_terms": "on",
        }

    def test_guest_can_reach_booking_details_before_signing_in(self):
        session = self.client.session
        session["selected_car_id"] = self.car.id
        session.save()

        response = self.client.post(reverse("bookings:booking_form"), self.booking_payload)

        booking = Booking.objects.get()
        self.assertIsNone(booking.user)
        self.assertRedirects(response, reverse("bookings:booking_details", args=[booking.id]))

        session = self.client.session
        self.assertEqual(session.get("guest_booking_id"), booking.id)

        detail_response = self.client.get(reverse("bookings:booking_details", args=[booking.id]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Sign In to Confirm Order")

    def test_confirming_guest_booking_after_login_assigns_user(self):
        session = self.client.session
        session["selected_car_id"] = self.car.id
        session.save()

        self.client.post(reverse("bookings:booking_form"), self.booking_payload)
        booking = Booking.objects.get()

        user = User.objects.create_user(
            username="guest-user@example.com",
            email="guest-user@example.com",
            password="testpass123",
        )
        self.client.force_login(user)

        with patch("bookings.views.send_booking_notification_email") as mock_send_notification:
            response = self.client.post(reverse("bookings:confirm_booking", args=[booking.id]), {"agree_terms": "on"})

        booking.refresh_from_db()
        self.assertEqual(booking.user, user)
        self.assertEqual(booking.status, "confirmed")
        mock_send_notification.assert_called_once()
        self.assertRedirects(response, reverse("home:order_success_detail", args=[booking.id]))

    def test_guest_only_accepts_terms_once_per_session(self):
        session = self.client.session
        session["selected_car_id"] = self.car.id
        session.save()

        first_response = self.client.get(reverse("bookings:booking_form"))
        # Terms are now required on confirm
        self.assertNotContains(first_response, 'id="agreeTerms"')

        self.client.post(reverse("bookings:booking_form"), self.booking_payload)

        second_response = self.client.get(reverse("bookings:booking_form"))
        self.assertNotContains(second_response, 'id="agreeTerms"')


@override_settings(STORAGES=TEST_STORAGES, RESEND_API_KEY="")
class BookingTermsAcceptanceTests(TestCase):
    def setUp(self):
        self.category = CarCategory.objects.create(name="Sedan")
        self.car = Car.objects.create(
            name="Toyota",
            model="Fielder",
            year=2023,
            category=self.category,
            price_per_day=90,
            seats=5,
        )
        self.user = User.objects.create_user(
            username="repeat@example.com",
            email="repeat@example.com",
            password="testpass123",
        )
        self.payload = {
            "pick_up_location": "Airport Road",
            "drop_off_location": "City Center",
            "pick_up_date": (timezone.now().date() + timedelta(days=3)).isoformat(),
            "pick_up_time": "09:00",
            "drop_off_date": (timezone.now().date() + timedelta(days=5)).isoformat(),
            "drop_off_time": "10:00",
            "additional_notes": "",
            "agree_terms": "on",
        }

    def test_signed_in_user_only_accepts_booking_terms_once(self):
        self.client.force_login(self.user)
        session = self.client.session
        session["selected_car_id"] = self.car.id
        session.save()

        first_response = self.client.get(reverse("bookings:booking_form"))
        # Terms are now required on confirm, not on form
        self.assertNotContains(first_response, 'id="agreeTerms"')

        response = self.client.post(reverse("bookings:booking_form"), self.payload)
        booking = Booking.objects.get()
        self.assertRedirects(response, reverse("bookings:booking_details", args=[booking.id]))

        # Confirm the booking with terms
        with patch("bookings.views.send_booking_notification_email"):
            confirm_response = self.client.post(
                reverse("bookings:confirm_booking", args=[booking.id]),
                {"agree_terms": "on"},
            )
        self.assertRedirects(confirm_response, reverse("home:order_success_detail", args=[booking.id]))

        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.profile.booking_terms_accepted_at)

        # Create another booking
        second_response = self.client.get(reverse("bookings:booking_form"))
        self.assertNotContains(second_response, 'id="agreeTerms"')


@override_settings(STORAGES=TEST_STORAGES, RESEND_API_KEY="")
class BookingHistoryViewTests(TestCase):
    def setUp(self):
        self.category = CarCategory.objects.create(name="Compact")
        self.car = Car.objects.create(
            name="Toyota",
            model="Vitz",
            year=2022,
            category=self.category,
            price_per_day=75,
            seats=5,
        )
        self.user = User.objects.create_user(
            username="history@example.com",
            email="history@example.com",
            password="testpass123",
        )

    def test_empty_booking_history_renders(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("bookings:booking_history"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Bookings Yet")
        self.assertContains(response, reverse("cars:car_list"))

    def test_booking_history_pagination_renders(self):
        for index in range(11):
            Booking.objects.create(
                user=self.user,
                car=self.car,
                pick_up_location=f"Pickup {index}",
                drop_off_location=f"Dropoff {index}",
                pick_up_date=timezone.now().date() + timedelta(days=index + 1),
                pick_up_time="09:00",
                drop_off_date=timezone.now().date() + timedelta(days=index + 2),
                drop_off_time="10:00",
                status="draft",
            )

        self.client.force_login(self.user)
        response = self.client.get(reverse("bookings:booking_history"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "?page=2")


@override_settings(STORAGES=TEST_STORAGES, RESEND_API_KEY="", BOOKING_NOTIFICATION_EMAILS=[])
class BookingNotificationRecipientTests(TestCase):
    def test_uses_active_superuser_email_when_no_recipients_are_configured(self):
        User.objects.create_superuser(
            username="owner@example.com",
            email="owner@example.com",
            password="testpass123",
        )

        self.assertEqual(get_booking_notification_recipients(), ["owner@example.com"])

    @override_settings(BOOKING_NOTIFICATION_EMAILS=["bookings@example.com"])
    def test_uses_configured_booking_notification_email_first(self):
        User.objects.create_superuser(
            username="owner@example.com",
            email="owner@example.com",
            password="testpass123",
        )

        self.assertEqual(get_booking_notification_recipients(), ["bookings@example.com"])
