"""
URL configuration for Diakorentalcars project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home.views import indexView as home_view
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('auth/', include('userAuth.urls')),
    path('accounts/', include('allauth.urls')),
    path('cars/', include('cars.urls')),
    path('bookings/', include('bookings.urls')),
    path('', home_view, name='home'),
    path(
        "favicon.ico",
        RedirectView.as_view(url=f"{settings.STATIC_URL}home/images/car2.png", permanent=False),
    ),
    path("dashboard/", include("dashboard.urls")),
]

if settings.DEBUG:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))

# âœ… FIX #2: Serve static and media files
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)


# âœ… FIX #2: Add error handlers for 404 and 500
handler404 = 'home.views.handler404'
handler500 = 'home.views.handler500'

