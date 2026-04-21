from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError
from cars.models import Car, CarCategory, CarRate, TripType
from .forms import CarForm
from dashboard.decorators import admin_required


def car_list_view(request):
    cars = Car.objects.select_related("category").all()
    categories = CarCategory.objects.all()
    triptypes = TripType.objects.all()
    selected_category = request.GET.get("category", "").strip()

    if selected_category:
        cars = cars.filter(category__slug=selected_category)

    rates = CarRate.objects.filter(car__in=cars)

    context = {
        'cars': cars,
        'categories': categories,
        'triptypes': triptypes,
        'rates': rates,
        'selected_category': selected_category,
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
        try:
            car.delete()
            messages.success(request, "Car deleted successfully.")
        except ProtectedError:
            messages.error(
                request,
                "This car cannot be deleted because it has existing bookings."
            )
        return redirect("cars:car_manage_list")

    return render(request, "cars/car_confirm_delete.html", {"car": car})


@admin_required
def car_bulk_delete_view(request):
    if request.method != "POST":
        return redirect("cars:car_manage_list")

    car_ids = request.POST.getlist("selected_ids")

    if not car_ids:
        messages.error(request, "Select at least one car to delete.")
        return redirect("cars:car_manage_list")

    deleted_count = 0
    failed_count = 0

    for car in Car.objects.filter(id__in=car_ids):
        try:
            car.delete()
            deleted_count += 1
        except ProtectedError:
            failed_count += 1

    if deleted_count:
        messages.success(request, f"{deleted_count} car(s) deleted successfully.")
    if failed_count:
        messages.error(
            request,
            f"{failed_count} car(s) could not be deleted because they have related bookings.",
        )

    return redirect("cars:car_manage_list")


@admin_required
def car_detail_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    # Get all rates for this car
    rates = car.rates.select_related('trip_type').all()
    
    context = {
        'car': car,
        'rates': rates,
    }
    
    return render(request, "cars/car_detail.html", context)
