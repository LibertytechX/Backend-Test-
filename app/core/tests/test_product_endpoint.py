
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Product, Category
from core.serializers import ProductSerializer
from django.contrib.auth.models import User
class ProductAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(name='Test Category')
        self.product_url = '/products/'
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            category=self.category
        )
    
    def test_create_product(self):
        url = self.product_url
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'price': 20.00,
            'category': self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_product_list(self):
        url = self.product_url
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Ensure that the list is not empty
    
    def test_get_single_product(self):
        url = f'{self.product_url}{self.product.id}/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)
    
    def test_update_product(self):
        url = f'{self.product_url}{self.product.id}/'
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'price': 25.00,
            'category': self.category.id
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Product')
    
    def test_delete_product(self):
        url = f'{self.product_url}{self.product.id}/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        #To Ensure the product is deleted
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
