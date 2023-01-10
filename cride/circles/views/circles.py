"""Circle views"""

# Django REST Framework
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

# Local modules
from cride.circles.models import Circle, Membership
from cride.circles.serializers import CircleModelSerializer
from cride.circles.permissions import IsCircleAdmin


class CircleViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """Circle view set."""

    serializer_class= CircleModelSerializer
# With this, we only look up circles using their slug_name
    lookup_field= "slug_name"

    def get_queryset(self):
        """Restrict list to public-only"""
        
        queryset= Circle.objects.all()
# Self.action comes from the viewsets
        if self.action == "list":
            return queryset.filter(is_public=True)
        return queryset
    
    def get_permissions(self):
        """Assign permissions based on actions"""
        
        permissions= [IsAuthenticated]
        if self.action in["updated", "partial_update"]:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]


    def perform_create(self, serializer):
        """Assign circle admin"""

        circle= serializer.save()
        user= self.request.user
        profile= user.profile

        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )






