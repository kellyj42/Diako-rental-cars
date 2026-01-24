from django.contrib import admin
from .models import CarCategory, Car

@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'category', 'price_per_day', 'is_available', 'is_featured']
    list_filter = ['category', 'is_available', 'is_featured', 'transmission', 'fuel_type']
    search_fields = ['name', 'model', 'description']
    list_editable = ['price_per_day', 'is_available', 'is_featured']
    filter_horizontal = []
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'model', 'year', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('price_per_day', 'price_per_week', 'price_per_month')
        }),
        ('Specifications', {
            'fields': ('seats', 'doors', 'transmission', 'fuel_type', 'engine_capacity', 'color')
        }),
        ('Images', {
            'fields': ('main_image', 'thumbnail')
        }),
        ('Features', {
            'fields': ('features', 'air_conditioning', 'bluetooth', 'gps', 'child_seat', 'sunroof')
        }),
        ('Availability', {
            'fields': ('is_available', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )