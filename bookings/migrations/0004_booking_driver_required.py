from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0003_booking_allow_guest_drafts"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="driver_required",
            field=models.BooleanField(default=False),
        ),
    ]
