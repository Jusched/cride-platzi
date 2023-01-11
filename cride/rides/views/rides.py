"""Ride views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

# Local modules
from cride.rides.serializers import CreateRideSerializer, RideModelSerializer
from cride.circles.permissions import IsActiveCircleMember
from cride.rides.permissions import IsRideOwner
from cride.circles.models import Circle


class RideViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    """Ride view set."""

    filter_backends= (SearchFilter, OrderingFilter)
    ordering= ("available_seats")
    ordering_fields= ("available_seats")
    search_fields= ("departure_location", "arrival_location")

    def dispatch(self, request, *args, **kwargs):
        """Verify that the Circle exists"""

        slug_name= kwargs["slug_name"]
        self.circle= get_object_or_404(Circle, slug_name=slug_name)
        return super(RideViewSet, self).dispatch(request, *args, **kwargs)
        
    def get_permissions(self):
        """Assign permission based on action."""

        permissions= [IsAuthenticated, IsActiveCircleMember]

        if self.action in ["update", "partial_update"]:
            permissions.append(IsRideOwner)
        return [p() for p in permissions]


    def get_serializer_context(self):
        """Add circle to serializer context."""

        context= super(RideViewSet, self).get_serializer_context()
        context["circle"] = self.circle
        return context

    def get_serializer_class(self):
        """Return serializer based on action."""

        if self.action == "create":
            return CreateRideSerializer
        return RideModelSerializer

    def get_queryset(self):
        """Return active circle rides."""

        return self.circle.ride_set.filter(
            is_active=True,
            available_seats__gte=1
        )

    


