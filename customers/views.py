from rest_framework import viewsets, permissions, filters
from .models import Customer
from .serializers import CustomerSerializer
from core.permissions import IsAdminOrServiceAdvisor

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing customers.
    Admins and Service Advisors can create/update/delete; all authenticated users can read.
    Implements search and filtering as per SRS FR-CUST-203.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'primary_phone', 'secondary_phone', 'email']
    ordering_fields = ['name', 'email', 'primary_phone']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrServiceAdvisor()]
        return [permissions.IsAuthenticated()]

    def perform_destroy(self, instance):
        # Soft delete: set is_active to False
        instance.is_active = False
        instance.save()
