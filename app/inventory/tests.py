from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product, Category, Order, OrderItem

User = get_user_model()

class CustomTokenObtainPairViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='firstuser@gmail.com', password='Testing123', name='First User')
        self.user.is_email_verified = True
        self.user.save()
        self.url = reverse('token')

    def test_token_obtain_pair(self):
        response = self.client.post(self.url, {'email': 'firstuser@gmail.com', 'password': 'Testing123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class UserRegistrationViewTest(APITestCase):

    def setUp(self):
        self.url = reverse('user_register')

    def test_user_registration(self):
        response = self.client.post(self.url, {'email': 'newuser@gmail.com', 'password': 'Testing123', 'name': 'New User'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

class ProductViewTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Category1', 
                                                slug='test-category')
        self.product = Product.objects.create(name='Product1', slug='test-product', 
                                              description='Test Description', 
                                              category=self.category)
        self.url = reverse('product_list_create')
        self.lst_url = reverse('product_list')

    def test_get_products(self):
        response = self.client.get(self.lst_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Product1')

    def test_post_product(self):
        data = {
            'name': 'New Product',
            'slug': 'new-product',
            'description': 'New Description',
            'price':200,
            'category': self.category.slug
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Product')

class CategoryViewTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.url = reverse('category_list_create')
        self.lst_url =reverse('category_list')

    def test_get_categories(self):
        response = self.client.get(self.lst_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Category')

    def test_post_category(self):
        data = {'name': 'New Category', 'slug': 'new-category'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Category')

class OrderViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='firstuser@gmail.com', password='Testing123', name='First User')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(name='Test Product', slug='test-product', 
                                              description='Test Description', 
                                              category=self.category)
        self.url = reverse('order_list_create')

    def test_get_orders(self):
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, product=self.product, quantity=1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['order_items'][0]['product']['name'], 'Test Product')
