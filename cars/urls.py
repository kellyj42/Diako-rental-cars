from django.urls import path
from .views import (
	car_list_view,
	car_manage_list_view,
	car_create_view,
	car_update_view,
	car_delete_view,
)

app_name='cars'
urlpatterns = [
	path('list/', car_list_view, name='car_list'),
	path('manage/', car_manage_list_view, name='car_manage_list'),
	path('manage/add/', car_create_view, name='car_create'),
	path('manage/<int:car_id>/edit/', car_update_view, name='car_update'),
	path('manage/<int:car_id>/delete/', car_delete_view, name='car_delete'),
    
]
