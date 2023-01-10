"""Circle permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Local modules
from cride.circles.models import Membership


class IsActiveCircleMember(BasePermission):
    """Allow access only to circle member.
    
    Expect that the views using this permission have a 'circle' attribute assigned.
    """

    def has_permission(self, request, view):
        """Verify user is an active member of the circle."""

        try:
            Membership.objects.filter(user=request.user, circle=view.circle, is_active=True)

        except Membership.DoesNotExist:
            return False
        return True


class IsSelfMember(BasePermission):
    """Allow access to only member owners."""

    def has_permission(self, request, view):
        """Let object permission grant access."""

# We know that the membership view has the get_object method.
        obj= view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        """Allow access only if the member is owned by the requesting user."""

        return request.user ==obj.user