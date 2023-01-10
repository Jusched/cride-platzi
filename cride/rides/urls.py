"""Rides urls."""

# Django REST Framework
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Local modules
from .views import rides as ride_views


router= DefaultRouter()
router.register(
    r'circles/(?P<slug_name>[a-zA-Z0-9_-]+)/members',
    ride_views.RideViewSet,
    basename="ride"
)

urlpatterns= [
    path("", include(router.urls))
]



