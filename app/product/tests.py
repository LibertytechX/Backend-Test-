from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Category

User = get_user_model()

class ProductViewSetTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email='oludarenathaniel@gmail.com', password='testpass')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            description='A high-end laptop',
            price=1200.00,
            category=self.category
        )
        self.valid_payload = {
            'name': 'Smartphone',
            'description': 'A new smartphone',
            'price': 800.00,
            'category': self.category.id
        }
        self.invalid_payload = {
            'name': '',
            'description': 'A new smartphone',
            'price': 800.00,
            'category': self.category.id
        }

        refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_product_authenticated(self):
        response = self.client.post(
            reverse('product-list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.post(
            reverse('product-list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_product_list(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_product_detail(self):
        response = self.client.get(reverse('product-detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_update_product_authenticated(self):
        response = self.client.put(
            reverse('product-detail', kwargs={'pk': self.product.pk}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Smartphone')

    def test_update_product_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.put(
            reverse('product-detail', kwargs={'pk': self.product.pk}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_product_authenticated(self):
        response = self.client.delete(
            reverse('product-detail', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.delete(
            reverse('product-detail', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CategoryViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='oludarenathaniel@gmail.com', password='testpass')
        self.category = Category.objects.create(name='Electronics')
        self.valid_payload = {
            'name': 'Home Appliances',
        }
        self.invalid_payload = {
            'name': '',
        }

        # Set up tokens
        refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_category_authenticated(self):
        response = self.client.post(
            reverse('category-list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.post(
            reverse('category-list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_category_list(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_category_detail(self):
        response = self.client.get(reverse('category-detail', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)

    def test_update_category_authenticated(self):
        response = self.client.put(
            reverse('category-detail', kwargs={'pk': self.category.pk}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'home appliances')

    def test_update_category_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.put(
            reverse('category-detail', kwargs={'pk': self.category.pk}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_category_authenticated(self):
        response = self.client.delete(
            reverse('category-detail', kwargs={'pk': self.category.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_category_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.delete(
            reverse('category-detail', kwargs={'pk': self.category.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_duplicate_category(self):
        response = self.client.post(
            reverse('category-list'),
            data={'name': 'electronics'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_category_name_normalized(self):
        response = self.client.post(
            reverse('category-list'),
            data={'name': '  New Category  '},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category = Category.objects.get(id=response.data['id'])
        self.assertEqual(category.name, 'new category')
