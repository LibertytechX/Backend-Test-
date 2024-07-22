from django.test import TestCase
from ..models import ProductCategory, Product


# Create your tests here.
class ProductCategoryModelTest(TestCase):

    def test_category_creation(self):
        """ Ensure a new category creation is successful. """
        category = ProductCategory.objects.create(name='Electronics')
        self.assertEqual(category.name, 'Electronics')
        self.assertEqual(str(category), category.name)
        self.assertIsInstance(category, ProductCategory)


class ProductModelTest(TestCase):

    def test_product_creation(self):
        """ Ensure a new product model creation is successful. """
        category = ProductCategory.objects.create(name='Electronics')
        product = Product.objects.create(
            name='iPhone 15',
            description=
            'A higher version of iPhone should be much better. Buy it.',
            price=1499.99,
            category=category)
        self.assertEqual(product.name, 'iPhone 15')
        self.assertEqual(
            product.description,
            'A higher version of iPhone should be much better. Buy it.')
        self.assertEqual(product.price, 1499.99)
        self.assertEqual(product.category, category)
        self.assertIsInstance(product, Product)
        self.assertEqual(str(product), 'iPhone 15')
