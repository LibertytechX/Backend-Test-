from django.test import TestCase
from django.urls import reverse
from rest_framework.status import *
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from .models import *

# Create your tests here.
from django.contrib.auth import get_user_model

User = get_user_model()
class TestViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create(email='test_user@gmail.com', password='test@password')
        self.test_user.save()
        self.category = Category.objects.create(name="test category")
        self.item = Products.objects.create(name='product one',price=10, description='test', category=self.category)
        self.ordereditem = OrderedItem.objects.create(product=self.item, quantity=5)
        self.order = Order.objects.create(user=self.test_user).items.add(self.ordereditem)
        
    
        self.access_token = AccessToken.for_user(self.test_user)
    
    def test_get_inventory_item_unauthenticated(self):
        url = reverse('products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED )
    
    def test_get_inventory_item_authenticated(self):
        url = reverse('products-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK )
    
    def test_create_inventory_product_unauthenticated(self):
        url = reverse('products-list')
        data = {'name':'new product', 'description':'test', 'price': 5}
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_create_inventory_product_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('products-list')
        data = {'name':'new product', 'description':'test', 'price': 5, 'category':self.category.id}
        
        response = self.client.post(url)
        response1 = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response1.status_code, HTTP_201_CREATED)
        
        
    
    def test_create_inventory_product_auth_with_missing_field(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('products-list')
        data = {'name':'new product', 'description':'test', 'price': 5}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_update_inventory_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('products-detail', args=[self.item.id])
        data = {
            'name':'new name', 'description':'new description', 'price':100, 'category':self.category.id
        }
        
        incomplete_data = {
            'description':'new description', 'price':100, 'category':self.category.id
        }
        response = self.client.put(url, data=data)
        response2 = self.client.put(url, data=incomplete_data)
        print(response.json())
        self.assertEqual(response.status_code, HTTP_200_OK)

        # put does not allow partial updates
        self.assertEqual(response2.status_code, HTTP_400_BAD_REQUEST)
    
    def test_partial_update_inventory_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('products-detail', args=[self.item.id])
        data = {
             'price':100,
        }
        response = self.client.patch(url, data=data)
        print(response.json())
        self.assertEqual(response.status_code, HTTP_200_OK)
    
    def test_soft_delete_inventory_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('products-detail', args=[self.item.id])
       
        response = self.client.delete(url)
        print(response.json())
        self.assertEqual(response.status_code, HTTP_200_OK)
    
    def test_hard_delete_inventory_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = f'http://localhost/api/v1/inventory/products/{self.item.id}/hard_delete/'
       
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
    
    

    def test_get_orders_item_unauthenticated(self):
        url = reverse('orders-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED )
    
    def test_get_orders_authenticated(self):
        url = reverse('orders-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        print(response.json())
        self.assertEqual(response.status_code, HTTP_200_OK )
    
    