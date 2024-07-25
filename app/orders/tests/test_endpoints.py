from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from orders.models import Order, OrderItem
from products.models import Category, Product


class OrderCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.order_create_url = reverse('order-create')
        
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            quantity=100,
            category=self.category
        )

    def test_create_order_success(self):
        payload = {
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 2
                }
            ]
        }
        response = self.client.post(self.order_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_create_order_invalid_product(self):
        payload = {
            'items': [
                {
                    'product': 999,  # Non-existent product ID
                    'quantity': 2
                }
            ]
        }
        response = self.client.post(self.order_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class OrderHistoryViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.order_history_url = reverse('order-history')
        
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            quantity=100,
            category=self.category
        )
        
        self.order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_get_order_history(self):
        response = self.client.get(self.order_history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['results']), 1)

    def test_order_history_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.order_history_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)