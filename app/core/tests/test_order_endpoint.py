# core/tests/test_order_endpoint.py
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from core.models import Order, Product, Category, OrderProduct
from core.serializers import OrderSerializer, ProductSerializer
from django.urls import reverse

class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        # Create a Category and Product for the Order
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            category=self.category
        )
        
        self.order_url = '/orders/'
        self.order_history_url = '/order-history/'
    
    def test_create_order(self):
        self.client.force_authenticate(user=self.user)  # Make sure user is authenticated
        url = reverse('order-list')
        data = {
            'products': [
                {'product': self.product.id, 'quantity': 2}  # Ensure data matches expected format
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_get_order_history(self):
        order = Order.objects.create(user=self.user)
        OrderProduct.objects.create(order=order, product=self.product, quantity=1)
        url = self.order_history_url
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure that at least one order is returned

    def test_unauthorized_create_order(self):
        url = reverse('order-list')
        data = {
            'products': [
                {'product': self.product.id, 'quantity': 2}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
