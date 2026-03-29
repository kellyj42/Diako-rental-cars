import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="additional_notes",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="booking",
            name="car",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="bookings",
                to="cars.car",
            ),
        ),
        migrations.AlterField(
            model_name="booking",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("confirmed", "Confirmed"),
                    ("cancelled", "Cancelled"),
                    ("completed", "Completed"),
                    ("expired", "Expired"),
                ],
                default="draft",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="booking",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="booking",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddIndex(
            model_name="booking",
            index=models.Index(fields=["user", "status"], name="bookings_bo_user_id_5a450c_idx"),
        ),
        migrations.AddIndex(
            model_name="booking",
            index=models.Index(fields=["car", "pick_up_date"], name="bookings_bo_car_id_b812d3_idx"),
        ),
    ]
