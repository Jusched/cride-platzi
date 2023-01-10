"""Ride views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

# Local modules
from cride.rides.serializers import CreateRideSerializer
from cride.circles.permissions import IsActiveCircleMember
from cride.circles.models import Circle



class RideViewSet(mixins.CreateModelMixin,
    viewsets.GenericViewSet):
    """Ride view set."""

    serializer_class= CreateRideSerializer
    permission_classes= [IsAuthenticated, IsActiveCircleMember]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the Circle exists"""

        slug_name= kwargs["slug_name"]
        self.circle= get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)




