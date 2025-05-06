from django.db import models

class Customer(models.Model):
    """
    Customer model for VMGMS.
    Fields and constraints per SRS FR-CUST-103/105 and best practices.
    """
    name = models.CharField(max_length=100, blank=False, null=False)
    address = models.TextField(max_length=500, blank=True, null=True)
    primary_phone = models.CharField(max_length=20, blank=False, null=False)
    secondary_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.primary_phone})"
