from datetime import date, time, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from bookings.models import Booking
from cars.models import Car, CarCategory


class CarDeleteViewTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            password="StrongPass123",
            is_staff=True,
        )
        self.customer = User.objects.create_user(
            username="customer@example.com",
            email="customer@example.com",
            password="StrongPass123",
        )
        self.category = CarCategory.objects.create(name="Sedan")
        self.car = Car.objects.create(
            name="Honda",
            model="Civic",
            year=2024,
            category=self.category,
            price_per_day=80,
        )

    def test_delete_view_shows_message_when_car_has_bookings(self):
        start_date = date.today() + timedelta(days=1)
        Booking.objects.create(
            user=self.customer,
            car=self.car,
            pick_up_location="Kampala",
            drop_off_location="Kampala",
            pick_up_date=start_date,
            pick_up_time=time(10, 0),
            drop_off_date=start_date + timedelta(days=1),
            drop_off_time=time(10, 0),
            status="confirmed",
        )

        self.client.force_login(self.admin_user)
        response = self.client.post(reverse("cars:car_delete", args=[self.car.id]))

        self.assertRedirects(response, reverse("cars:car_manage_list"))
        self.assertTrue(Car.objects.filter(id=self.car.id).exists())
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("cannot be deleted" in str(message) for message in messages))
