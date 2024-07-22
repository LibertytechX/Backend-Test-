from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Order, OrderProduct
from products.models import Product, ProductCategory


class OrderProductModelTest(TestCase):

    def setUp(self):
        self.category = ProductCategory.objects.create(name='Electronics')
        self.product = Product.objects.create(name='Smartphone',
                                              description='A description',
                                              price=499.99,
                                              category=self.category)

    def test_order_product_creation(self):
        """ Ensure model creates an Order Product successfully. """
        order_product = OrderProduct.objects.create(product=self.product,
                                                    quantity=10)
        self.assertEqual(order_product.product.name, 'Smartphone')
        self.assertEqual(len(OrderProduct.objects.all()), 1)
        self.assertEqual(str(order_product),
                         f"{self.product} - {order_product.status}")
        self.assertIsInstance(order_product.product, Product)


class OrderModelTest(TestCase):

    def setUp(self):
        self.category = ProductCategory.objects.create(name='Electronics')
        self.product = Product.objects.create(name='Smartphone',
                                              description='A description',
                                              price=499.99,
                                              category=self.category)

    def test_order_creation_with_one_product(self):
        """ Ensure creation of an order with one product. """
        user = get_user_model().objects.create_user(email='mail@example.com',
                                                    password='somepassword')
        order_product = OrderProduct.objects.create(product=self.product,
                                                    quantity=10)
        order = Order.objects.create(user=user)
        order.products.add(order_product)
        order.save()

        self.assertEqual(len(Order.objects.all()), 1)
        self.assertEqual(len(order.products.all()), 1)

    def test_order_creation_with_multiple_products(self):
        """ Ensure creation of an order with multiple products. """
        user = get_user_model().objects.create_user(email='mail@example.com',
                                                    password='somepassword')
        order_product_one = OrderProduct.objects.create(product=self.product,
                                                        quantity=10)
        order_product_two = OrderProduct.objects.create(product=self.product,
                                                        quantity=15)
        order_product_three = OrderProduct.objects.create(product=self.product,
                                                          quantity=12)
        order = Order.objects.create(user=user)
        order.products.add(order_product_one)
        order.products.add(order_product_two)
        order.products.add(order_product_three)
        order.save()

        self.assertEqual(len(Order.objects.all()), 1)
        self.assertEqual(len(order.products.all()), 3)
