from django.shortcuts import render
from cars.models import Car, CarCategory, CarRate, TripType


def car_list_view(request):
    cars = Car.objects.all()
    categories = CarCategory.objects.all()
    triptypes = TripType.objects.all()
    rates = CarRate.objects.all()

    context = {
        'cars': cars,
        'categories': categories,
        'triptypes': triptypes,
        'rates': rates,
    }
    
    return render(request, 'cars/cars.html', context)