from django.urls import path
from . import views

app_name = 'bookings'
urlpatterns = [
     path("selectedCar/", views.selectedVehicle, name="car"),
     path("booking/", views.booking_form_view, name="booking_form"),
     path("cancel-car/", views.cancel_selected_car, name="cancel_car"),
     path("details/<int:booking_id>/", views.booking_details_view, name="booking_details"),
     path("save-draft/", views.save_booking_draft, name="save_draft"),
     path('confirm-booking/<int:booking_id>/',views.confirm_booking,name='confirm_booking'),
     path("my-bookings/", views.booking_history_view, name="booking_history"),
     path("cancel/<int:booking_id>/", views.cancel_booking_view, name="cancel_booking"),
     path("manage/", views.booking_manage_list_view, name="booking_manage_list"),
     path("manage/<int:booking_id>/status/", views.booking_update_status_view, name="booking_update_status"),
     path("manage/<int:booking_id>/delete/", views.booking_delete_view, name="booking_delete"),
     path("manage/bulk-delete/", views.booking_bulk_delete_view, name="booking_bulk_delete"),


] 
