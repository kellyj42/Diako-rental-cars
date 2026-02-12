from django.urls import path
from . import views

app_name='userAuth'

urlpatterns = [
    path('login/', views.login_view, name ='login'),
    path('signup/', views.signup_view, name='signup'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('email-verification/', views.email_verification_view, name='email_verification'),
    path('logout/', views.logout_view, name='logout'),
    path("verify-email/<uidb64>/<token>/",views.verify_email_view,name="verify_email"),
    path("resend-verification/", views.resend_verification_email, name="resend_verification"),
    path("password_reset_link/", views.password_reset_link, name="password_reset_link"),
    path("profile/", views.profile_view, name="profile"),
    path("manage/", views.user_manage_list_view, name="user_manage_list"),
    path("manage/add/", views.user_create_view, name="user_create"),
    path("manage/<int:user_id>/edit/", views.user_update_view, name="user_update"),
    path("manage/<int:user_id>/delete/", views.user_delete_view, name="user_delete"),
]