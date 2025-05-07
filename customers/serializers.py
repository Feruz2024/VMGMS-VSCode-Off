from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'address', 'primary_phone', 'secondary_phone', 'email', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        # Enforce unique, case-insensitive email
        if Customer.objects.filter(email__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("A customer with this email already exists.")
        return value

    def validate_primary_phone(self, value):
        # Basic format check: allow digits, spaces, ()-+
        import re
        if not re.match(r'^[\d\s\-\+\(\)]+$', value):
            raise serializers.ValidationError("Enter a valid phone number (digits, spaces, ()-+ allowed).")
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name must not be empty.")
        return value
