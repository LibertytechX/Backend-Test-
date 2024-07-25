from decimal import Decimal

from django.test import TestCase

from products.models import Category, Product


class CategoryModelTests(TestCase):
    def test_category_str(self):
        category = Category.objects.create(name='Electronics')
        self.assertEqual(str(category), 'Electronics')


class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')

    def test_product_str(self):
        product = Product.objects.create(
            name='Smartphone',
            description='A high-end smartphone',
            price=Decimal('999.99'),
            quantity=10,
            category=self.category
        )
        self.assertEqual(str(product), 'Smartphone')

    def test_product_price_decimal_places(self):
        product = Product.objects.create(
            name='Laptop',
            description='A powerful laptop',
            price=Decimal('1999.999'),
            quantity=5,
            category=self.category
        )
        self.assertNotEqual(product.price, Decimal('2000.00'))
