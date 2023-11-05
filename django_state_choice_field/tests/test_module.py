from django.test import TestCase

from django_state_choice_field.exceptions import (
    InvalidStateEnumError,
    InvalidTransitionError,
)

from .models import Orders, PaymentStatus


class StateChoiceFieldTest(TestCase):
    def test_default_value(self):
        order = Orders.objects.create(product_name="Test Product")
        self.assertEqual(order.status, PaymentStatus.NOT_STARTED)

    def test_valid_value(self):
        order = Orders.objects.create(
            product_name="Test Product", status=PaymentStatus.COMPLETED
        )
        self.assertEqual(order.status, PaymentStatus.COMPLETED)

    def test_valid_value_as_string(self):
        order = Orders.objects.create(product_name="Test Product", status="completed")
        self.assertEqual(order.status, PaymentStatus.COMPLETED)

    def test_invalid_value(self):
        with self.assertRaises(InvalidStateEnumError):
            Orders.objects.create(product_name="Test Product", status="invalid")

    def test_invalid_state_change(self):
        order = Orders.objects.create(
            product_name="Test Product", status=PaymentStatus.COMPLETED
        )
        with self.assertRaises(InvalidTransitionError):
            order.status = PaymentStatus.NOT_STARTED
            order.save()
