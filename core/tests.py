from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.request import Request
from .permissions import IsAdmin, IsServiceAdvisor, IsTechnician

User = get_user_model()

class PermissionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # Create groups
        self.admin_group = Group.objects.create(name='Admin')
        self.sa_group = Group.objects.create(name='ServiceAdvisor')
        self.tech_group = Group.objects.create(name='Technician')
        # Create users
        self.admin_user = User.objects.create_user(username='admin', password='test')
        self.sa_user = User.objects.create_user(username='sa', password='test')
        self.tech_user = User.objects.create_user(username='tech', password='test')
        self.regular_user = User.objects.create_user(username='regular', password='test')
        # Assign groups
        self.admin_user.groups.add(self.admin_group)
        self.sa_user.groups.add(self.sa_group)
        self.tech_user.groups.add(self.tech_group)

    def test_is_admin_permission(self):
        drf_request = Request(self.factory.get('/'))
        drf_request.user = self.admin_user
        self.assertTrue(IsAdmin().has_permission(drf_request, None))
        drf_request.user = self.sa_user
        self.assertFalse(IsAdmin().has_permission(drf_request, None))

    def test_is_service_advisor_permission(self):
        drf_request = Request(self.factory.get('/'))
        drf_request.user = self.sa_user
        self.assertTrue(IsServiceAdvisor().has_permission(drf_request, None))
        drf_request.user = self.admin_user
        self.assertFalse(IsServiceAdvisor().has_permission(drf_request, None))

    def test_is_technician_permission(self):
        drf_request = Request(self.factory.get('/'))
        drf_request.user = self.tech_user
        self.assertTrue(IsTechnician().has_permission(drf_request, None))
        drf_request.user = self.admin_user
        self.assertFalse(IsTechnician().has_permission(drf_request, None))
