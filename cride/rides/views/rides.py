"""Ride views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

# Local modules
from cride.rides.serializers import CreateRideSerializer, RideModelSerializer, JoinRideSerializer, EndRideSerializer, CreateRideRatingSerializer
from cride.circles.permissions import IsActiveCircleMember
from cride.rides.permissions import IsRideOwner, IsNotRideOwner
from cride.circles.models import Circle
from datetime import timezone

class RideViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
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

        if self.action in ["update", "partial_update", "finish"]:
            permissions.append(IsRideOwner)
        if self.action == "join":
            permissions.append(IsNotRideOwner)
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
        if self.action == "update":
            return JoinRideSerializer
        if self.action == "finish":
            return EndRideSerializer
        if self.action == "rate":
            return CreateRideRatingSerializer
        return RideModelSerializer

    def get_queryset(self):
        """Return active circle rides."""

        return self.circle.ride_set.filter(
            is_active=True,
            available_seats__gte=1
        )

    @action(detail=True, methods=["POST"])
    def join(self, request, *args, **kwargs):
        """Add requesting user to ride."""

        ride= self.get_object()
        serializer_class= self.get_serializer_class()
        serializer= serializer_class(
            ride,
            data= {"passenger": request.user.pk},
            context={"ride": ride, "circle": self.circle},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data= RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=["POST"])
    def finish(self, request, *args, **kwargs):
        """Called by owners to finish a ride."""

        ride= self.get_object()
        serializer_class= self.get_serializer_class()
        serializer= serializer_class(
            ride,
            data={"is_active": False, "current_time": timezone.now()},
            context=self.get_serializer_context(),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data= RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def rate(self, request, *args, **kwargs):
        """Rate a ride."""

        ride= self.get_object()
        serializer_class= self.get_serializer_class()
        context= self.get_serializer_context()

        context["ride"]= ride
        serializer= serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        ride = serializer.save()
        data= RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_201_CREATED)

