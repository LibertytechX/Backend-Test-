from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Category, Product

class ProductViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            quantity=100,
            category=self.category
        )
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', args=[self.product.id])

    def test_get_product_list(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['results']), 1)

    def test_get_product_detail(self):
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Test Product')

    def test_create_product_unauthorized(self):
        payload = {
            'name': 'New Product',
            'description': 'New Description',
            'price': 15.00,
            'quantity': 50,
            'category': self.category.id
        }
        response = self.client.post(self.product_list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)