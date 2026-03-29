from django.db import IntegrityError
from django.db import migrations
from django.utils.text import slugify


def seed_car_categories(apps, schema_editor):
    CarCategory = apps.get_model("cars", "CarCategory")

    categories = [
        {
            "name": "Coasters",
            "icon": "fas fa-bus",
            "description": "Suitable for tours, events, and larger group travel.",
        },
        {
            "name": "Sedans",
            "icon": "fas fa-car",
            "description": "Comfortable everyday and business travel vehicles.",
        },
        {
            "name": "SUVs",
            "icon": "fas fa-truck-monster",
            "description": "Spacious vehicles for family trips and upcountry travel.",
        },
        {
            "name": "Vans",
            "icon": "fas fa-van-shuttle",
            "description": "Ideal for airport transfers and group movement.",
        },
    ]

    for category in categories:
        slug = slugify(category["name"])
        car_category = (
            CarCategory.objects.filter(slug=slug).first()
            or CarCategory.objects.filter(name=category["name"]).first()
        )

        if car_category is None:
            try:
                car_category = CarCategory.objects.create(
                    slug=slug,
                    name=category["name"],
                    icon=category["icon"],
                    description=category["description"],
                )
            except IntegrityError:
                # If the slug already exists under a slightly different name,
                # reuse that row instead of failing the whole migration.
                car_category = CarCategory.objects.get(slug=slug)

        updates = []
        if car_category.slug != slug:
            car_category.slug = slug
            updates.append("slug")
        if car_category.name != category["name"]:
            car_category.name = category["name"]
            updates.append("name")
        if car_category.icon != category["icon"]:
            car_category.icon = category["icon"]
            updates.append("icon")
        if car_category.description != category["description"]:
            car_category.description = category["description"]
            updates.append("description")
        if updates:
            car_category.save(update_fields=updates)


def unseed_car_categories(apps, schema_editor):
    CarCategory = apps.get_model("cars", "CarCategory")
    CarCategory.objects.filter(slug__in=["coasters", "sedans", "suvs", "vans"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0005_remove_car_main_image"),
    ]

    operations = [
        migrations.RunPython(seed_car_categories, unseed_car_categories),
    ]
