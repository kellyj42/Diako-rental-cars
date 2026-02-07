from django.urls import path
from .views import car_list_view

app_name='cars'
urlpatterns = [
	path('list/', car_list_view, name='car_list'),
    
]
