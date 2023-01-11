"""Celery tasks."""

# Django REST Framework
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

# Celery
from celery import Celery

# Local modules
from cride.users.models import User

# Utilities
import jwt
import time
from datetime import timedelta

app = Celery()


def gen_verification_token(user):
    """Create a JWT that the user can use to verify its account"""
    
    exp= timezone.now() + timedelta(days=2)
    payload= {
        "user": user.username,
        "exp": int(exp.timestamp()),
        "type": "email_confirmation"
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

@app.task(name="send_confirmation_email", max_retries=3)
def send_confirmation_email(user_pk):
    """Send account verification link to the given user."""

    for i in range(30):
        time.sleep(1)
        print("Sleeping", i)

    user= User.objects.get(pk=user_pk)
    verification_token= gen_verification_token(user)

    subject= f"Welcome @{user.username}! Verify your account to start using Comparte Ride."
    from_email= "Comparte Ride <noreply@comparteride.com>"
    content= render_to_string(
        "emails/users/account_verification.html", 
        {"token": verification_token, "user": user}
    )
    msg= EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()
