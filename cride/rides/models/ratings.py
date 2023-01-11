"""Ratings model."""

# Django REST Framework
from django.db import models

# Local modules
from cride.utils.models import CRideModel


class Rating(CRideModel):
    """Ride rating.
    
    Rates are entities that store the rating a user
    gave to a ride and its owner. It ranges from 
    1 to 5 and it affects the rider's reputation.
    """

    ride= models.ForeignKey(
        "rides.Ride",
        on_delete=models.CASCADE,
        related_name="rated_ride"
    )
    circle= models.ForeignKey(
        "circles.Circle",
        on_delete=models.CASCADE
    )
    rating_user= models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        help_text="User that rates the ride.",
        related_name="rating_user"
    )

    comments= models.TextField(blank=True)
    rating= models.FloatField(default=1)

    def __str__(self) -> str:
        return 
