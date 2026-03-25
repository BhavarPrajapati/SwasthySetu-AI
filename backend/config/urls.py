"""
URL Configuration for alzheimer_screening project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/screening/', include('apps.screening.urls')),
]
