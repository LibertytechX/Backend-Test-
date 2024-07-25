from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Product, Category
from django.contrib.auth import get_user_model
from django.urls import reverse


class ProductTests(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            email="admin@test.com", password='password')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            price=1000.00,
            quantity=10,
            description='A high-performance laptop',
            category=self.category
        )
        self.list_url = reverse('product-list')
        self.detail_url = reverse('product-detail', args=[self.product.id])
        self.create_url = reverse('create-product')
        self.update_delete_url = reverse(
            'product-update-delete', args=[self.product.id])

    def test_create_product(self):
        data = {
            'name': 'Smartphone',
            'price': 800.00,
            'quantity': 15,
            'description': 'A high-end smartphone',
            'category': self.category.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.latest('id').name, 'Smartphone')

    def test_list_products(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_products(self):
        response = self.client.get(self.list_url, {'search': 'Laptop'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['results'][0]['name'], 'Laptop')

    def test_get_product_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Laptop')

    def test_get_product_not_found(self):
        url = reverse('product-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product(self):
        data = {'name': 'Updated Laptop'}
        response = self.client.patch(
            self.update_delete_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Laptop')

    def test_delete_product(self):
        response = self.client.delete(self.update_delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 0)

    def test_delete_product_not_found(self):
        url = reverse('product-update-delete', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
