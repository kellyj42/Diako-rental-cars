from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.indexView, name='home'),
    path('details/', views.bookingDetailsView, name='details'),
    path('order-success/', views.orderSuccessView, name='order_success'),
]