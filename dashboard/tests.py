from datetime import date, time, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from bookings.models import Booking
from cars.models import Car, CarCategory


class DashboardHomeTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            password="StrongPass123",
            is_staff=True,
        )
        self.category = CarCategory.objects.create(name="SUV")
        self.car = Car.objects.create(
            name="Toyota",
            model="RAV4",
            year=2024,
            category=self.category,
            price_per_day=100,
        )

    def test_dashboard_counts_draft_bookings_as_pending(self):
        today = date.today() + timedelta(days=1)
        Booking.objects.create(
            user=self.admin_user,
            car=self.car,
            pick_up_location="Kampala",
            drop_off_location="Kampala",
            pick_up_date=today,
            pick_up_time=time(9, 0),
            drop_off_date=today + timedelta(days=2),
            drop_off_time=time(9, 0),
            status="draft",
        )

        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("dashboard:home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["pending_bookings"], 1)
