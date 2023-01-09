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
            Membership.objects.get(user=request.user, circle=view.circle, is_active=True)

        except Membership.DoesNotExist:
            return False
        return True