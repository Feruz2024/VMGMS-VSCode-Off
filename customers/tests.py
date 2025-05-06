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
