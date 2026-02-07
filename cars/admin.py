from django.contrib import admin
from .models import (
    CarCategory,
    Car,
    TripType,
    CarRate,
)

# -------------------------
# INLINE: CAR RATES INSIDE CAR
# -------------------------
class CarRateInline(admin.TabularInline):
    model = CarRate
    extra = 1
    autocomplete_fields = ['trip_type']
    fields = (
        'trip_type',
        'destination',
        'price',
        'fuel_included',
        'driver_included',
        'notes',
    )


# -------------------------
# CAR CATEGORY ADMIN
# -------------------------
@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)


# -------------------------
# CAR ADMIN
# -------------------------
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'year',
        'category',
        'drive_type',
        'fuel_type',
        'transmission',
        'is_available',
        'is_featured',
    )

    list_filter = (
        'category',
        'drive_type',
        'fuel_type',
        'transmission',
        'is_available',
        'is_featured',
    )

    search_fields = (
        'name',
        'model',
        'year',
    )

    list_editable = (
        'is_available',
        'is_featured',
    )

    inlines = [CarRateInline]

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'model',
                'year',
                'category',
                'description',
            )
        }),
        ('Specifications', {
            'fields': (
                'seats',
                'doors',
                'drive_type',
                'fuel_type',
                'transmission',
                'engine_capacity',
                'color',
            )
        }),
        ('Features', {
            'fields': (
                'air_conditioning',
                'bluetooth',
                'gps',
                'child_seat',
                'sunroof',
                'features',
            )
        }),
        ('Images', {
            'fields': (
               
                'thumbnail',
            )
        }),
        ('Availability & Visibility', {
            'fields': (
                'is_available',
                'is_featured',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


# -------------------------
# TRIP TYPE ADMIN
# -------------------------
@admin.register(TripType)
class TripTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# -------------------------
# CAR RATE ADMIN
# -------------------------
@admin.register(CarRate)
class CarRateAdmin(admin.ModelAdmin):
    list_display = (
        'car',
        'trip_type',
        'destination',
        'price',
        'fuel_included',
        'driver_included',
    )

    list_filter = (
        'trip_type',
        'fuel_included',
        'driver_included',
    )

    search_fields = (
        'car__name',
        'car__model',
        'destination',
    )

    autocomplete_fields = (
        'car',
        'trip_type',
    )

    fieldsets = (
        ('Car & Service', {
            'fields': (
                'car',
                'trip_type',
                'destination',
            )
        }),
        ('Pricing', {
            'fields': (
                'price',
                'fuel_included',
                'driver_included',
            )
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )
