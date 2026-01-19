from django.urls import path
from . import views

app_name='userAuth'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('email-verification/', views.email_verification_view, name='email_verification'),
    path('logout/', views.logout_view, name='logout'),
]