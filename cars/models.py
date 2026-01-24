from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator

class CarCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
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

class Car(models.Model):
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
        ('cng', 'CNG'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    model = models.CharField(max_length=100, blank=True)
    year = models.PositiveIntegerField()
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE, related_name='cars')
    
    # Pricing
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    price_per_week = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    price_per_month = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    # Specifications
    seats = models.PositiveIntegerField(default=4)
    doors = models.PositiveIntegerField(default=4)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='automatic')
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, default='petrol')
    engine_capacity = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    
    # Images
    main_image = models.ImageField(upload_to='cars/main/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='cars/thumbnails/', blank=True, null=True)
    
    # Features
    features = models.TextField(blank=True, help_text="Comma-separated features list")
    air_conditioning = models.BooleanField(default=True)
    bluetooth = models.BooleanField(default=True)
    gps = models.BooleanField(default=False)
    child_seat = models.BooleanField(default=False)
    sunroof = models.BooleanField(default=False)
    
    # Availability
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Additional Info
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_available', 'is_featured']),
            models.Index(fields=['category', 'price_per_day']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.year})"
    
    @property
    def display_name(self):
        if self.model:
            return f"{self.name} {self.model}"
        return self.name
    
    @property
    def feature_list(self):
        if self.features:
            return [f.strip() for f in self.features.split(',')]
        return []
    
    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.main_image:
            return self.main_image.url
        return '/static/defaults/car-thumbnail.jpg'