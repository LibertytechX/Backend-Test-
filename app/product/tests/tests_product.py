from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import User
from product.models import Category, Product, Order, OrderProduct
from rest_framework_simplejwt.tokens import RefreshToken

class APIViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser('admin@test.com', 'Admin@pass123')
        self.regular_user = User.objects.create_user('user@test.com', 'User@pass123')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price="10.00",
            stock=10,
            category=self.category,
            sku="STM3021"
        )
        self.order = Order.objects.create(user=self.regular_user)
        OrderProduct.objects.create(order=self.order, product=self.product, quantity=1, price=self.product.price)

    def test_category_list_view(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_category_create_view(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('category-create')
        data = {'name': 'New Category'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_category_detail_view(self):
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Test Category')

    def test_category_update_view(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('category-update', kwargs={'pk': self.category.pk})
        data = {'name': 'Updated Category'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_category_delete_view(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('category-update', kwargs={'pk': self.category.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_product_list_view(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_product_create_view(self):
        self.client.force_authenticate(user=self.admin_user)

        url = reverse('product-create')
        data = {
            "name": "Samsung Galaxy S21 5G 6.2'' (128GB ROM 8GB RAM) Single Sim - Gray",
            "description": "Brand / Model Samsung Galaxy S21 G991UOS Android 11CPU Qualcomm Snapdragon 888 Octa Core 2.8GHzGPU Adrenov660RAM 8 GBROM 128 GB",
            "price": "380.00",
            "category": self.category.pk,
            "stock": 10,
            "sku": "SMT2021"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_product_detail_view(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_update_view(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('product-update', kwargs={'pk': self.product.pk})
        data = {
            "name": "Samsung Galaxy S21 5G 6.2'' (128GB ROM 8GB RAM) Single Sim - Gray",
            "description": "Brand / Model Samsung Galaxy S21 G991UOS Android 11CPU Qualcomm Snapdragon 888 Octa Core 2.8GHzGPU Adrenov660RAM 8 GBROM 128 GB",
            "price": "380.00",
            "category": self.category.id,
            "stock": 200,
            "sku": "SMT2021"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()

    def test_product_delete_view(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('product-delete', kwargs={'pk': self.product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_order_list_view(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('products' in response.data['data'])
        self.assertEqual(len(response.data['data']['products']), 1)

    def test_order_create_view(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('order-create')
        data = {
            "status": "pending",
            "shipping_address": "Opposite Catholic Church Shavon Mile Six",
            "billing_address": "456 Oak Rd, Jalingo, Taraba State",
            "products": [
            {
                "product_id": self.product.pk,
                "quantity": 2
            }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_order_update_view(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('order-update', kwargs={'pk': self.order.pk})
        new_product = Product.objects.create(
            name='New Product',
            description='New Description',
            price="20.00",
            stock=10,
            category=self.category,
            sku="STM3011"
        )
        data = {
            "status": "pending",
            "shipping_address": "Opposite Catholic Church Shavon Mile Six",
            "billing_address": "456 Oak Rd, Jalingo, Taraba State",
            "products": [
                {"product_id": self.product.pk,"quantity": 1},
                {'product_id': new_product.pk, 'quantity': 2}
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()

    def test_order_list_view(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('products', response.data['data'])
        self.assertEqual(len(response.data['data']['products']), 1)
