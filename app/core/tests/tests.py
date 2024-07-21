import json
from django.urls import reverse
from django.test import TestCase, TransactionTestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from products.models import Category, Product
from orders.models import Order

User = get_user_model()

class CategoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='testuser', email='example@gmail.com', password='testpassword')
        self.token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.category_url = reverse('category-list-create')

    def get_jwt_token(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'email': 'example@gmail.com', 'password': 'testpassword'}, format='json')
        return response.data['access']

    def test_create_category(self):
        data = {"category_name": "Gadgets"}
        response = self.client.post(self.category_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().category_name, 'Gadgets')

    def test_list_categories(self):
        Category.objects.create(category_name='Gadgets')
        response = self.client.get(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['category_name'], 'Gadgets')

class ProductTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='testuser', email='example@gmail.com', password='testpassword')
        self.token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.category = Category.objects.create(category_name='Gadgets')
        self.product_url = reverse('product-list-create')

    def get_jwt_token(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'email': 'example@gmail.com', 'password': 'testpassword'}, format='json')
        return response.data['access']

    def test_create_product(self):
        data = {
            "name": "SmartWatch",
            "description": "Powerful smartwatch for techies",
            "price": 1500.00,
            "stock": 10,
            "category": {
                "category_name": "Gadgets"
            }
        }
        response = self.client.post(self.product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'SmartWatch')

    def test_list_products(self):
        Product.objects.create(
            name="SmartWatch",
            description="Powerful smartwatch for techies",
            price=1500.00,
            stock=10,
            category=self.category
        )
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'SmartWatch')

    def test_retrieve_product(self):
        product = Product.objects.create(
            name="SmartWatch",
            description="Powerful smartwatch for techies",
            price=1500.00,
            stock=10,
            category=self.category
        )
        url = reverse('product-detail', args=[product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'SmartWatch')

    def test_delete_product(self):
        product = Product.objects.create(
            name="SmartWatch",
            description="Powerful smartwatch for techies",
            price=1500.00,
            stock=10,
            category=self.category
        )
        url = reverse('product-detail', args=[product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
        
class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='testuser', email='example@gmail.com', password='testpassword')
        self.token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.category = Category.objects.create(category_name='Gadgets')
        self.product = Product.objects.create(
            name="SmartWatch",
            description="A smart watch",
            price=199.99,
            stock=100,
            category=self.category
        )

        self.order_create_url = reverse('order-create')
        self.order_history_url = reverse('order-history')

    def get_jwt_token(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'email': 'example@gmail.com', 'password': 'testpassword'}, format='json')
        return response.data['access']

    def test_create_order(self):
        data = {
            "products": [self.product.id],
            "quantity": 2
        }
        response = self.client.post(self.order_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.products.first(), self.product)
        self.assertEqual(order.quantity, 2)

    def test_order_history(self):
        Order.objects.create(user=self.user, quantity=2)
        response = self.client.get(self.order_history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        order = response.data['results'][0]
        self.assertEqual(order['quantity'], 2)
        self.assertEqual(order['user'], self.user.id)
