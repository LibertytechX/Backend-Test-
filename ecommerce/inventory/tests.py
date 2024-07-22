from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Category, Product, Order
from rest_framework_simplejwt.tokens import RefreshToken

class UserTests(APITestCase):
    
    def test_register(self):
        url = reverse('register')
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'testuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse('login')
        User.objects.create_user(username='testuser', password='testpassword')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class ProductTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Log in and get JWT token
        self.client.login(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Laptop", description="A personal computer", price=1000, category=self.category)

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_product(self):
        self.authenticate()
        url = reverse('product-list')
        data = {'name': 'Smartphone', 'description': 'A mobile phone', 'price': 500, 'category': self.category.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_list_products(self):
        self.authenticate()
        url = reverse('product-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_product(self):
        self.authenticate()
        url = reverse('product-detail', args=[self.product.id])
        data = {'name': 'Laptop Pro', 'description': 'A professional laptop', 'price': 1500, 'category': self.category.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        self.authenticate()
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Log in and get JWT token
        self.client.login(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Laptop", description="A personal computer", price=1000, category=self.category)

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_order(self):
        self.authenticate()
        url = reverse('order-create')
        data = {'user':self.user.id, 'products': [self.product.id], 'quantity': 1}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_history(self):
        self.authenticate()
        order = Order.objects.create(user=self.user, quantity=1)
        order.products.add(self.product)
        url = reverse('order-history')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
