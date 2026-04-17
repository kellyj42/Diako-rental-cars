from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userAuth", "0003_profile_last_seen_bookings_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="booking_terms_accepted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
