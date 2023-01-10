"""Circle invitation managers."""

# Django REST Framework
from django.db import models

# Local modules
import random
from string import ascii_uppercase, digits


class InvitationManager(models.Manager):
    """Invtation manager.
    
    Used to handle code creation.
    """
    CODE_LENGTH= 10

    def create(self, **kwargs):
        """Handles code creation."""

        pool= ascii_uppercase + digits
        code= kwargs.get("code", "".join(random.choices(pool, k=self.CODE_LENGTH )))
    
# If there is a code being sent and it already exists, it creates a new one.
        while self.filter(code=code).exists():
            code= "".join(random.choices(pool, k=self.CODE_LENGTH))
        kwargs["code"]= code
        return super(InvitationManager, self).create(**kwargs)