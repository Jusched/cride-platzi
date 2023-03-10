"""Users serializers"""

# Django
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models import fields

# Tasks
from cride.taskapp.tasks import send_confirmation_email

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Models
from cride.users.models import User, Profile
from cride.users.serializers.profiles import ProfileModelSerializer

# Utilities
import jwt


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)
    class Meta:
        """Meta class"""
        model= User
        fields= (
            "username", 
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "profile"         
        )

class UserSignupSerializer(serializers.Serializer):
    """User signup serializer
    
    Handles sign up data validation and user/profile creation.
    """
    email= serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())]
            )
    username= serializers.CharField(
        min_length=4, 
        max_length=20,
        validators=[
            UniqueValidator(queryset=User.objects.all())]
        )
    # Phone number
    phone_regex= RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +11 1111111111. Up to 15 digits."
    )
    phone_number= serializers.CharField(validators=[phone_regex])
    
    # Password
    password= serializers.CharField(min_length=8, max_length=64)
    password_confirmation= serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name= serializers.CharField(min_length=2, max_length=30)
    last_name= serializers.CharField(min_length=2, max_length=30)


    def validate(self, data):
        """Verify password match"""

        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(password=data["password"])
        return data


    def create(self, data):
        """Handle user and profile creation"""

        data.pop("password_confirmation")
        user= User.objects.create_user(**data, is_verified=False, is_client=True)
        profile= Profile.objects.create(user=user)
        send_confirmation_email.delay(user_pk=user.pk)
        return user


class UserLoginSerializer(serializers.Serializer):
    """User login Serializer

        Handles the user request data.
    """
    
    email= serializers.EmailField()
    password= serializers.CharField(min_length=8, max_length=64)
     
    def validate(self, data):
        """Verify credentials"""
        user= authenticate(username=data["email"], password=data["password"])
        
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_verified:
            raise serializers.ValidationError("Account hasn't been activated.")

        self.context["user"] = user
        return data


    def create(self, data):
        """Generate or retrieve new token"""

        token, created= Token.objects.get_or_create(user=self.context["user"])
        return self.context["user"], token.key


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer"""

    token= serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid"""

        try:
            payload= jwt.decode(data, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Verification link has expired.")

        except jwt.PyJWTError:
            raise serializers.ValidationError("Invalid token")

        if payload["type"] != "email_confirmation":
            raise serializers.ValidationError("Invalid token")

        self.context["payload"]= payload
        return data

# We overwrite this so we don't have to return the instance as Django makes us do that.
    def save(self):
        """Update user's verified status"""

        payload= self.context["payload"]
        user= User.objects.get(username=payload["user"])
        user.is_verified= True
        user.save()



