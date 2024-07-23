from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include('djoser.urls')),
    path("api/auth/", include('djoser.urls.authtoken')),
    path('api/auth/', include('allauth.urls')),
    path("api/v1/", include('HoinkyPass.urls')),
]

