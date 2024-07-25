
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Product

class ProductAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.product1 = Product.objects.create(name='Product 1', price=10.00)
        self.product2 = Product.objects.create(name='Product 2', price=20.00)
        self.product3 = Product.objects.create(name='Another Product', price=30.00)

    def test_product_search(self):
        response = self.client.get('/products/', {'search': 'Product'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # We expect Only 'Product 1' and 'Product 2' should be returned

    def test_product_pagination(self):
        response = self.client.get('/products/', {'page': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('next' in response.data)  # Check if there is a next page
        self.assertTrue('previous' not in response.data)  # Check if there is no previous page
        self.assertEqual(len(response.data['results']), 10)  # Verify the number of items per page

