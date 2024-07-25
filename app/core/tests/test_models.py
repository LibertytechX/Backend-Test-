from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Product, Order, OrderProduct

class ProductModelTest(TestCase):
    
    def setUp(self):
        self.product = Product.objects.create(name='Test Product', price=19.99)

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 19.99)

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Product')


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.order = Order.objects.create(user=self.user)

    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertIsNotNone(self.order.created_at)

    def test_order_str(self):
        self.assertEqual(str(self.order), f"Order {self.order.id} by testuser")


class OrderProductModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(name='Test Product', price=19.99)
        self.order = Order.objects.create(user=self.user)
        self.order_product = OrderProduct.objects.create(order=self.order, product=self.product, quantity=5)

    def test_order_product_creation(self):
        self.assertEqual(self.order_product.order, self.order)
        self.assertEqual(self.order_product.product, self.product)
        self.assertEqual(self.order_product.quantity, 5)

    def test_order_product_str(self):
        self.assertEqual(str(self.order_product), '5 of Test Product in Order 1')

    def test_order_product_related_name(self):
        # Test related_name for Order model
        self.assertIn(self.order_product, self.order.order_products.all())
