from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.indexView, name='home'),
    path('order-success/', views.orderSuccessView, name='order_success'),
    path('order-success/<int:booking_id>/', views.orderSuccessView, name='order_success_detail'),
    path('about-us/', views.about_us_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('about-us/our-story/', views.our_story_view, name='our_story'),
    path('about-us/team/', views.team_view, name='team'),
    path('about-us/careers/', views.careers_view, name='careers'),
    path('faqs/', views.faqs_view, name='faqs'),
    path('contact/', views.contact_view, name='contact'),
]