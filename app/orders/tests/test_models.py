from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from orders.models import Order, OrderItem
from products.models import Category, Product


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Smartphone',
            description='A high-end smartphone',
            price=Decimal('999.99'),
            quantity=10,
            category=self.category
        )

    def test_order_str(self):
        order = Order.objects.create(user=self.user)
        self.assertEqual(str(order), f"Order {order.id} by {self.user.email}")

    def test_order_total_amount(self):
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, product=self.product, quantity=2)
        self.assertEqual(order.total_amount, Decimal('1999.98'))


class OrderItemModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Smartphone',
            description='A high-end smartphone',
            price=Decimal('999.99'),
            quantity=10,
            category=self.category
        )
        self.order = Order.objects.create(user=self.user)

    def test_order_item_str(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )
        expected_str = f"2 x Smartphone in Order {self.order.id}"
        self.assertEqual(str(order_item), expected_str)

    def test_order_item_total(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )
        self.assertEqual(order_item.item_total, Decimal('1999.98'))
