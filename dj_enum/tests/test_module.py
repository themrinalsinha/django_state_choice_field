from django.test import TestCase

from dj_enum.exceptions import InvalidStateEnumError

from .models import Orders, PaymentStatus


class DJEnumStateChoiceFieldTest(TestCase):
    def test_default_value(self):
        order = Orders.objects.create(product_name="Test Product")
        self.assertEqual(order.status, PaymentStatus.NOT_STARTED)

    def test_valid_value(self):
        order = Orders.objects.create(
            product_name="Test Product", status=PaymentStatus.COMPLETED
        )
        self.assertEqual(order.status, PaymentStatus.COMPLETED)

    def test_invalid_value(self):
        with self.assertRaises(InvalidStateEnumError):
            Orders.objects.create(product_name="Test Product", status="invalid")
