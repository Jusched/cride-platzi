"""Membership serializers."""

# Django REST Framework
from rest_framework import serializers
from django.db.models import fields
from django.utils import timezone

# Local modules
from cride.circles.models import Membership, Invitation
from cride.users.serializers import UserModelSerializer


class MembershipModelSerializer(serializers.ModelSerializer):
    """Member model serializer."""

    user= UserModelSerializer(read_only=True)
    invited_by= serializers.StringRelatedField()
    joined_at= serializers.DateTimeField(source="created", read_only=True)

    class Meta:
        model= Membership
        fields= (
            "user", "is_admin", "is_active",
            "used_invitations", "remaining_invitations",
            "invited_by", "rides_taken", "rides_offered",
            "joined_at"
        )
        read_only_fields= (
            "user", "used_invitation", "invited_by"
            "rides_taken", "rides_offered"
        )


class AddMemberSerializer(serializers.Serializer):
    """Add member serializer.
    
    Handle the addition of a new member to a circle.
    Circle object must be provided in the context.
    """

    invitation_code= serializers.CharField(min_length=8)
# Since we are sending the request, Django can know the User without having to validate it as any other field.
    user= serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, data):
        """Verify user isn't a member already."""

        circle= self.context["circle"]
        user= data

        q= Membership.objects.filter(circle=circle, user=user)

        if q.exists():
            raise serializers.ValidationError("User is already a member of this circle.")

    def validate_code(self, data):
        """Verify code exists and it's related to the circle."""

        try:
            invitation= Invitation.objects.get(
                code=data,
                circle=self.context["circle"],
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializers.ValidationError("Invalid invitation code.")
        
        self.context["invitation"]= invitation
        return data

    def validate(self, data):
        """Verify if the circle is capable of accepting the new member."""

        circle= self.context["circle"]
        if circle.is_limited and circle.members.count() >= circle.members_limit:
            raise serializers.ValidationError("Circle has reached its member limit.")
        
        return data

    def create(self, data):
        """Create new circle member."""

        circle= self.context["circle"]
        invitation= self.context["invitation"]
# This one is included already thanks to the "HiddenField" serializer.
        user= data["user"]

        now = timezone.now()

    # Member creation
        member= Membership.objects.create(
            user=user,
            profile=user.profile,
            circle=circle,
            invited_by=invitation.issued_by
        )

    # Update invitation
        invitation.used_by= user
        invitation.used= True
        invitation.used_at= now
        invitation.save()

    # Update issuer data
        issuer= Membership.objects.get(
            user=invitation.issued_by,
            circle=circle
        )
        issuer.used_invitations += 1
        issuer.remaining_invitations -+ 1
        issuer.save()

        return member
