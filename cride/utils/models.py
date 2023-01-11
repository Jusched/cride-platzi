"""Django models utilties."""

from django.db import models

class CRideModel(models.Model):
    """Comparte Ride base models.
    
    CRideModel is an abstract base class from which every 
    other model in the project will inherit. This class 
    provides every table with the following attributes:

        - created: DateTime = Store datetime in which the 
        object was created.
        - modified: DateTime = Store the last datetime in
        which the object was modified.
    """
    
    created= models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='DateTime in which the object was created'
    )
    modified= models.DateTimeField(
        'modified at',
        auto_now=True,  # Only applies when the model is called.
        help_text='DateTime in which the object was last modified'
    )

    class Meta:
        """Meta option."""
        abstract= True

        get_latest_by= 'created'
        ordering= ['-created', '-modified'] 



