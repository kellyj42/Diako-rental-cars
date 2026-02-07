from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator


# -------------------------
# CAR CATEGORY
# -------------------------
class CarCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, default='fas fa-car')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Car Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# -------------------------
# CAR
# -------------------------
class Car(models.Model):
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Rental price per day in USD.")

    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
        ('semi-automatic', 'Semi-Automatic'),
    ]

    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
    ]

    DRIVE_TYPE_CHOICES = [
        ('2wd', '2 Wheel Drive'),
        ('4wd', '4 Wheel Drive'),
    ]

    # Basic info
    name = models.CharField(max_length=200)
    model = models.CharField(max_length=100, blank=True)
    year = models.PositiveIntegerField()
    category = models.ForeignKey(
        CarCategory,
        on_delete=models.CASCADE,
        related_name='cars'
    )

    # Specifications
    seats = models.PositiveIntegerField(default=4)
    doors = models.PositiveIntegerField(default=4)
    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES,
        default='automatic'
    )
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_TYPE_CHOICES,
        default='petrol'
    )
    drive_type = models.CharField(
        max_length=10,
        choices=DRIVE_TYPE_CHOICES,
        default='2wd'
    )
    engine_capacity = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)

    # Features (as per document)
    air_conditioning = models.BooleanField(default=True)
    bluetooth = models.BooleanField(default=True)
    gps = models.BooleanField(default=False)
    child_seat = models.BooleanField(default=False)
    sunroof = models.BooleanField(default=False)

    features = models.TextField(
        blank=True,
        help_text="Comma-separated extra features"
    )

 
    
    thumbnail = models.ImageField(
        upload_to='cars/thumbnails/',
        blank=True,
        null=True
    )

    # Availability
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # Meta
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_available', 'is_featured']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.name} {self.model} ({self.year})"

    @property
    def display_name(self):
        return f"{self.name} {self.model}" if self.model else self.name

    @property
    def feature_list(self):
        return [f.strip() for f in self.features.split(',')] if self.features else []

    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return '/static/images/car-thumbnail.jpg'


# -------------------------
# TRIP / SERVICE TYPE
# -------------------------
class TripType(models.Model):
    """
    Examples:
    - In Town
    - Out of Town
    - Airport Pickup / Drop-off
    - Long Distance Trip
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# -------------------------
# CAR RATES (CORE OF RATE CARD)
# -------------------------
class CarRate(models.Model):
    """
    Represents the scanned document pricing exactly:
    - Different prices per car
    - Per trip type
    - With or without fuel
    - Optional destination (e.g. Kampala)
    """

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='rates'
    )

    trip_type = models.ForeignKey(
        TripType,
        on_delete=models.CASCADE,
        related_name='rates'
    )

    destination = models.CharField(
        max_length=150,
        blank=True,
        help_text="Optional destination e.g. Kampala"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    fuel_included = models.BooleanField(default=False)
    driver_included = models.BooleanField(default=True)

    notes = models.TextField(
        blank=True,
        help_text="Any special conditions"
    )

    class Meta:
        unique_together = (
            'car',
            'trip_type',
            'destination',
            'fuel_included'
        )

    def __str__(self):
        fuel = "With Fuel" if self.fuel_included else "Without Fuel"
        dest = f" - {self.destination}" if self.destination else ""
        return f"{self.car} | {self.trip_type}{dest} | {fuel}"
