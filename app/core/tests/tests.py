from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from core.models import User, Product, Category, Order
from rest_framework_simplejwt.tokens import RefreshToken


class UserTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'password123',
            're_password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_login_user(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url, {
            'email': 'testuser@example.com',
            'password': 'password123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_logout_user(self):
        self.client.post(self.register_url, self.user_data, format='json')
        login_response = self.client.post(self.login_url, {
            'email': 'testuser@example.com',
            'password': 'password123'
        }, format='json')
        refresh_token = login_response.data['refresh']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_response.data['access'])
        response = self.client.post(self.logout_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)


class CategoryTests(APITestCase):
    def setUp(self):
        self.category_url = reverse('category-list')
        self.user = User.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='password123',
            first_name='Admin',
            last_name='User'
        )
        self.category_data = {'name': 'Shirts'}

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_create_category(self):
        self.authenticate()
        response = self.client.post(self.category_url, self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_categories(self):
        self.authenticate()
        Category.objects.create(name='Shirts')
        response = self.client.get(self.category_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_category(self):
        self.authenticate()
        category = Category.objects.create(name='Shirts')
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        self.authenticate()
        category = Category.objects.create(name='Shirts')
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.put(url, {'name': 'Pants'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        self.authenticate()
        category = Category.objects.create(name='Shirts')
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Shirts')
        self.product_url = reverse('product-list')
        self.user = User.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='password123',
            first_name='Admin',
            last_name='User'
        )
        self.client.force_authenticate(user=self.user)
        self.product_data = {
            'product_name': 'Polo Shirt',
            'description': 'A nice polo shirt',
            'price': 29.99,
            'category': self.category.id
        }
        self.update_data = {
            'product_name': 'Updated Polo Shirt',
            'description': 'An updated polo shirt description',
            'price': 39.99,
            'category': self.category.id
        }

    def test_create_product(self):
        response = self.client.post(self.product_url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_products(self):
        Product.objects.create(
            product_name='Polo Shirt',
            description='A nice polo shirt',
            price=29.99,
            category=self.category
        )
        response = self.client.get(self.product_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product(self):
        product = Product.objects.create(
            product_name='Polo Shirt',
            description='A nice polo shirt',
            price=29.99,
            category=self.category
        )
        url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        product = Product.objects.create(
            product_name='Polo Shirt',
            description='A nice polo shirt',
            price=29.99,
            category=self.category
        )
        url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.put(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        product = Product.objects.create(
            product_name='Polo Shirt',
            description='A nice polo shirt',
            price=29.99,
            category=self.category
        )
        url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_products_with_pagination(self):
        for i in range(15):
            Product.objects.create(
                product_name=f'Product {i}',
                description=f'Description for product {i}',
                price=29.99 + i,
                category=self.category
            )
        response = self.client.get(self.product_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Default page size is 10

    def test_search_products(self):
        Product.objects.create(
            product_name='Searchable Product',
            description='Description for searchable product',
            price=29.99,
            category=self.category
        )
        response = self.client.get(self.product_url, {'search': 'Searchable'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)


class OrderTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Shirts')
        self.product = Product.objects.create(
            product_name='Polo Shirt',
            description='A nice polo shirt',
            price=29.99,
            category=self.category
        )
        self.user = User.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='password123',
            first_name='Admin',
            last_name='User'
        )
        self.order_url = reverse('order-list')
        self.order_history_url = reverse('order-history')
        self.order_data = {
            'user': self.user.id,
            'products': [self.product.id],
            'quantity': 5
        }
        self.client.force_authenticate(user=self.user)

    def test_create_order(self):
        response = self.client.post(self.order_url, self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_orders(self):
        Order.objects.create(user=self.user, quantity=5)
        response = self.client.get(self.order_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_history(self):
        Order.objects.create(user=self.user, quantity=5)
        response = self.client.get(self.order_history_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)