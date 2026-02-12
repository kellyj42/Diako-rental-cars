from django.shortcuts import render, redirect, get_object_or_404
from cars.models import Car, CarCategory, CarRate, TripType
from .forms import CarForm
from dashboard.decorators import admin_required


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


@admin_required
def car_manage_list_view(request):
    cars = Car.objects.select_related("category").all()
    return render(request, "cars/car_manage_list.html", {"cars": cars})


@admin_required
def car_create_view(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("cars:car_manage_list")
    else:
        form = CarForm()

    return render(request, "cars/car_form.html", {"form": form, "mode": "create"})


@admin_required
def car_update_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect("cars:car_manage_list")
    else:
        form = CarForm(instance=car)

    return render(request, "cars/car_form.html", {"form": form, "mode": "update", "car": car})


@admin_required
def car_delete_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        car.delete()
        return redirect("cars:car_manage_list")

    return render(request, "cars/car_confirm_delete.html", {"car": car})