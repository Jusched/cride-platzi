"""Users views"""

# Django REST framework
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

# Local modules
from cride.users.serializers import UserLoginSerializer, UserModelSerializer, UserSignupSerializer, AccountVerificationSerializer, ProfileModelSerializer
from cride.circles.serializers import CircleModelSerializer
from cride.users.models import User
from cride.circles.models import Circle
from cride.users.permissions import IsAccountOwner


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """User view set
    
    Handles sign up, login and account verification.
    """

    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class= UserModelSerializer
    lookup_field= "username"

    def get_permissions(self):
        """Assign permissions based on action."""

        if self.action in ["signup", "login", "verify"]:
            permissions= [AllowAny]

        elif self.action == ["retrieve", "updated", "partial_update"]:
            permissions= [IsAuthenticated, IsAccountOwner]
        else:
            permissions= [IsAuthenticated]
        return [p() for p in permissions]


    @action(detail=False, methods=["post"])
# The name of this method will be used in the URL.
    def login(self, request):
        """User login"""

        serializer= UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user, token= serializer.save()
        data= {
            "user": UserModelSerializer(user).data,
            "access_token": token
        }
        return Response(data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=["post"])
    def signup(self, request):
        """User sign up"""

        serializer= UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user= serializer.save()
        data= UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    
    @action(detail=False, methods=["POST"])
    def verify(self, request):
        """Account verification"""
        
        serializer= AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data= {
            "message": "Congratulations, now you can use Comparte Ride!"
        }
        return Response(data, status=status.HTTP_200_OK)


    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""

        response= super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles= Circle.objects.filter(
            members=request.user,
            membership__is_active=True
        )
        data= {
            "user": response.data,
            "circles": CircleModelSerializer(circles, many=True).data
        }
        response.data= data
        return response

    
    @action(detail=True, methods=["PUT", "PATCH"])
    def profile(self, request, *args, **kwargs):
        """Update profile data"""
        
        user= self.get_object()
        profile= user.profile
        partial= request.method == "PATCH"
        serializer= ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
# We user UserModel since we will make it have a Profile instance. 
        data= UserModelSerializer(user).data
        return Response(data)