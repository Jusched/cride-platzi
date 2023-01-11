"""Invitations tests."""

# Django REST Framework
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# Local modules
from cride.circles.models import Invitation, Circle, Membership
from cride.users.models import User


class InvitationsManagerTestCase(TestCase):
    """Invitations manager test case."""

    def setUp(self):
        """Test case set up."""

        self.user= User.objects.create(
            first_name= "velo",
            last_name= "Betancur",
            email= "velo@test.com",
            username= "velo",
            password= "admin12345"
        )
        self.circle= Circle.objects.create(
            name="Gaviotas",
            slug_name="gaviota",
            about="Circulo el barrio Gaviotas",
            is_verified=True
        )

    def test_code_generation(self):
        """Random codes should be generated automatically."""

        invitation= Invitation.objects.create(
            issued_by= self.user,
            circle= self.circle
        )
        self.assertIsNotNone(invitation.code)


class MemberInvitationsAPITestCase(APITestCase):
    """Member invitation API Test case."""

    def setUp(self):
        """Test case set up."""

        self.user= User.objects.create(
            first_name= "velo",
            last_name= "Betancur",
            email= "velo@test.com",
            username= "velo",
            password= "admin12345"
        )
        self.circle= Circle.objects.create(
            name="Gaviotas",
            slug_name="gaviota",
            about="Circulo el barrio Gaviotas",
            is_verified=True
        )
        self.membership = Membership.objects.create(
            user=self.user, profile=self.user.profile,
            circle=self.circle, remaining_invitations=10
        )
        self.token = Token.objects.create(user=self.user).key

