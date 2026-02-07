from django.shortcuts import render
from cars.models import Car
from content.content import services,achievements,vehicles,nav_links

# Create your views here.

def indexView(request):
    # Check session for a selected car (set by bookings.selectedVehicle)
    selected_car = None
    selected_car_id = request.session.get('selected_car_id')

    if selected_car_id:
        try:
            selected_car = Car.objects.get(id=selected_car_id)
        except Car.DoesNotExist:
            selected_car = None

    return render(request, 'home/homepage.html',
                {
                 "services": services,
                 "achievements": achievements,
                 "vehicles": vehicles,
                 "nav_links": nav_links,
                 "selected_car": selected_car,
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

def about_us_view(request):
    return render(request, 'aboutpage.html',{
                    "nav_links": nav_links
             })
def services_view(request):
    return render(request, 'home/includes/servicespage.html',
                 {
                    "services": services, 
                    "nav_links": nav_links
             })
