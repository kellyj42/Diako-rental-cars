from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userAuth", "0002_profile_phone_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="last_seen_bookings_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
