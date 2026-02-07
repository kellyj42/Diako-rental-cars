# bookings/admin.py
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "car",
        "pick_up_date",
        "drop_off_date",
        "status",
        "created_at",
    )

    list_filter = ("status", "pick_up_date")
    search_fields = ("user__email", "car__name")
    list_editable = ("status",)
