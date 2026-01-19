from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
from .content.content import services,achievements,vehicles,nav_links
# Create your views here.

def indexView(request):
    return render(request, 'homepage.html',
                {
                 "services": services,
                 "achievements": achievements,
                 "vehicles": vehicles,
                 "nav_links": nav_links,
                })

def bookingDetailsView(request):
    return render(request, 'home/booking_details.html')

def orderSuccessView(request):
    # You can pass order details here from session, database, or URL parameters
    context = {
        'confirmation_number': 'ORD-2025-001234',
        'pickup_date': 'January 25, 2025 - 10:00 AM',
        'dropoff_date': 'January 30, 2025 - 10:00 AM',
        'duration': '5 Days',
        'vehicle_name': 'Toyota Land Cruiser Prado 2022',
        'vehicle_type': '7-Seater SUV',
        'license_plate': 'DRC-2024-001',
        'customer_name': 'John Doe',
        'customer_email': 'john.doe@example.com',
        'customer_phone': '+1 (555) 123-4567',
        'pickup_location': 'Downtown Office',
    }
    return render(request, 'home/order_success.html', context)

@requires_csrf_token
def page_not_found(request, exception):
    return render(request, '404.html', status=404)

@requires_csrf_token
def server_error(request):
    return render(request, '500.html', status=500)