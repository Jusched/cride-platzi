"""User model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utilities
from cride.utils.models import CRideModel


class User(CRideModel, AbstractUser):
    """User model.
    
    Extends from Django's AbstractUser, change the username field
    to email and add some extra fields.    
    """

    email= models.EmailField(
        'email address.',
        unique= True,
        error_messages={
            'unique': 'A user with that email already exists.',
        }
    )

    phone_regex= RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +11 1111111111. Up to 15 digits."
# It can start with a '+', can start with 1 digit and can contain from 9 to 15 characters.
    )
    phone_number= models.CharField(validators=[phone_regex] ,max_length=15, blank=True)

# Login option is now the email.
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= ['username', 'first_name', 'last_name']
    is_client= models.BooleanField(
        'client status',
        default=True,
        help_text=(
            "Help easily distinguish users and perform queries."
            "Clients are the main type of user."
        )
    )
    is_verified= models.BooleanField(
        'verified',
        default=False,
        help_text="Set to true when the email has verified its email address."
    )

    def __str__(self):
        """Return username"""
        return self.username

    def get_short_name(self):
        """Return username"""
        return self.username





