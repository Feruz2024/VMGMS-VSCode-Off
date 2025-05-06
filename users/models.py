from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model for VMGMS, extending Django's AbstractUser.
    Add additional fields here if needed in the future.
    """
    # Example: add custom fields below
    # phone_number = models.CharField(max_length=20, blank=True, null=True)
    pass
