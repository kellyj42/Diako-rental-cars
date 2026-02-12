from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.indexView, name='home'),
    path('order-success/', views.orderSuccessView, name='order_success'),
    path('order-success/<int:booking_id>/', views.orderSuccessView, name='order_success_detail'),
    path('about-us/', views.about_us_view, name='about'),
    path('services/', views.services_view, name='services'),
]