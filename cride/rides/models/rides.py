"""Rides models."""

# Django REST Framework
from django.db import models

# Local modules
from cride.utils.models import CRideModel


class Ride(CRideModel):
    """Ride model."""
# Since the rides are the most important thing of our project, we set it to NULL
    offered_by= models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    offered_in= models.ForeignKey("circles.Circle", on_delete=models.SET_NULL, null=True)

    passengers= models.ManyToManyField("users.User", related_name="passangers")

    available_seats= models.PositiveSmallIntegerField(default=1)
    comments= models.TextField(blank=True)

    departure_location= models.CharField(max_length=255)
    departure_date= models.DateTimeField(auto_now_add=True)
    arrival_location= models.CharField(max_length=255)
    arrival_date= models.DateTimeField(auto_now=True)

    rating= models.FloatField(null=True)
    
    is_active= models.BooleanField(
        "active status",
        default=True,
        help_text="Used for cancelling the ride or making it as finished."
    )

    def __str__(self) -> str:
        return f"{self.departure_location} to {self.arrival_location} | {self.departure_date.strftime('%a %d, %b')} {self.departure_date.strftime('%I:%M %p')} - {self.arrival_date.strftime('%I:%M')}"