from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.indexView, name='home'),
    path('details/', views.bookingDetailsView, name='details'),
    path('order-success/', views.orderSuccessView, name='order_success'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('client-dashboard/', views.client_dashboard_view, name='client_dashboard'),
    path('about-us/', views.about_us_view, name='about'),
    path('services/', views.services_view, name='services'),
]