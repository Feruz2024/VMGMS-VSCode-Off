from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
# API tests for Customer endpoints
from django.contrib.auth.models import Group

class CustomerAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='test')
        self.sa = User.objects.create_user(username='sa', password='test')
        self.tech = User.objects.create_user(username='tech', password='test')
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        sa_group, _ = Group.objects.get_or_create(name='ServiceAdvisor')
        tech_group, _ = Group.objects.get_or_create(name='Technician')
        self.admin.groups.add(admin_group)
        self.sa.groups.add(sa_group)
        self.tech.groups.add(tech_group)
        self.client = APIClient()
        self.customer_data = {
            'name': 'Jane Smith',
            'address': '456 Elm St',
            'primary_phone': '555-9876',
            'secondary_phone': '555-4321',
            'email': 'jane@example.com',
        }

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_admin_can_create_customer(self):
        self.authenticate(self.admin)
        response = self.client.post('/api/customers/', self.customer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Jane Smith')

    def test_sa_can_create_customer(self):
        self.authenticate(self.sa)
        response = self.client.post('/api/customers/', self.customer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tech_cannot_create_customer(self):
        self.authenticate(self.tech)
        response = self.client.post('/api/customers/', self.customer_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_customers_requires_auth(self):
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_soft_delete_customer(self):
        self.authenticate(self.admin)
        create = self.client.post('/api/customers/', self.customer_data)
        cid = create.data['id']
        response = self.client.delete(f'/api/customers/{cid}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check is_active is now False
        from customers.models import Customer
        customer = Customer.objects.get(id=cid)
        self.assertFalse(customer.is_active)
from django.test import TestCase
from .models import Customer
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class CustomerModelTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'name': 'John Doe',
            'address': '123 Main St',
            'primary_phone': '555-1234',
            'secondary_phone': '555-5678',
            'email': 'john@example.com',
        }

    def test_create_customer_success(self):
        customer = Customer.objects.create(**self.valid_data)
        self.assertEqual(customer.name, 'John Doe')
        self.assertEqual(customer.primary_phone, '555-1234')
        self.assertEqual(customer.secondary_phone, '555-5678')
        self.assertEqual(customer.email, 'john@example.com')
        self.assertTrue(customer.is_active)
        self.assertIsNotNone(customer.created_at)
        self.assertIsNotNone(customer.updated_at)

    def test_required_fields(self):
        # Name required (blank)
        data = self.valid_data.copy()
        data['name'] = ''
        customer = Customer(**data)
        with self.assertRaises(ValidationError):
            customer.full_clean()
        # Primary phone required (blank)
        data = self.valid_data.copy()
        data['primary_phone'] = ''
        customer = Customer(**data)
        with self.assertRaises(ValidationError):
            customer.full_clean()
        # Email required (blank)
        data = self.valid_data.copy()
        data['email'] = ''
        customer = Customer(**data)
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_email_uniqueness(self):
        Customer.objects.create(**self.valid_data)
        with self.assertRaises(IntegrityError):
            Customer.objects.create(**self.valid_data)

    def test_optional_fields(self):
        data = self.valid_data.copy()
        data['address'] = ''
        data['secondary_phone'] = ''
        customer = Customer.objects.create(**data)
        self.assertEqual(customer.address, '')
        self.assertEqual(customer.secondary_phone, '')
