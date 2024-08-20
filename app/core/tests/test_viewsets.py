import jwt

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from app.settings import SECRET_KEY 
from core.models import Category, User, Product, Order
from core.serializers import CategorySerializer, UserSerializer, ProductSerializer, OrderSerializer


class TokenAcessRefreshViewTests(APITestCase):
    def test_get_user_access_token_success(self):
        """
        Test success retrieving new access token for a user
        """
        url = reverse('user-register')
        data = {
            'email': 'Test2@mail.com',
            'password': 'Pass@2ndversion',
            'name': 'TestDev'
        }
        signup_response = self.client.post(url, data)
        url = reverse('token_refresh')
        data = {
            'refresh': signup_response.data['data']['tokens']['refresh']
        }
        refresh_response = self.client.post(url, data)
        token_payload = jwt.decode(str(refresh_response.data['access']), SECRET_KEY, algorithms=["HS256"])
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertEqual(token_payload['user_id'], signup_response.data['data']['id'])
        self.assertEqual(token_payload['token_type'], 'access')
        
        


class SignUpLoginViewTests(APITestCase):
    def test_register_user_success(self):
        """
        Test success creating/registering a user
        """
        url = reverse('user-register')
        data = {
            'email': 'Test2@mail.com',
            'password': 'Pass@2ndversion',
            'name': 'TestDev'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['email'], 'Test2@mail.com'.lower())
        self.assertEqual(len(response.data['data']['tokens']), 2)
    
    def test_user_login_success(self):
        """
        Test success authenticating a user
        """
        url = reverse('user-register')
        data = {
            'email': 'Test2@mail.com',
            'password': 'Pass@2ndversion',
            'name': 'TestDev'
        }
        response = self.client.post(url, data)
        url = reverse('user-login')
        data = {
            'email': data['email'],
            'password': data['password']
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['tokens']), 2)
    
    
    def test_token_blacklist_success(self):
        """
        Test success blacklisting user's refresh token
        """
        url = reverse('user-register')
        data = {
            'email': 'Test2@mail.com',
            'password': 'Pass@2ndversion',
            'name': 'TestDev'
        }
        signup_response = self.client.post(url, data)
        url = reverse('user-logout')
        data = {
            'refresh': signup_response.data['data']['tokens']['refresh']
        }
        logout_response = self.client.post(url, data)
        
        url = reverse('token_refresh')
        data = {
            'refresh': signup_response.data['data']['tokens']['refresh']
        }
        refresh_response = self.client.post(url, data)
        self.assertEqual(signup_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
          
        
    
    
class AuthViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@mail.com",
            password="@Test2024.",
            name="Test"
        )
        self.client.force_authenticate(user=self.user)
        self.new_password = '@NewPass2025'
        
    
    def test_get_autheneticated_user_success(self):
        """
        Test success retrieving authenticated user in session
        """
        url = reverse('user-me')
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['id'], self.user.id)
    
    
    def test_get_unautheneticated_user_failure(self):
        """
        Test failure retrieving unauthenticated user in session
        """
        self.client.logout()
        url = reverse('user-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    
    def test_get_user_password_reset_token(self):
        """
        Test success retrieving user password reset token
        """
        self.client.logout()
        url = reverse('user-request-password-reset')
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        data = {
            'email': self.user.email
        }
        response = self.client.post(url, data)
        token = jwt.decode(str(response.data['data']), SECRET_KEY, algorithms=["HS256"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(token['id'], self.user.id)
        
        
    def test_reset_user_password_token_success(self):
        """
        Test success resetting user password
        """
        self.client.logout()
        url = reverse('user-request-password-reset')
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        data = {
            'email': self.user.email
        }
        response = self.client.post(url, data)
        
        url = reverse('user-reset-password')
        data = {
            'password': self.new_password,
            'token': response.data['data']
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class UserViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@mail.com",
            password="@Test2024.",
            name="Test"
        )
        self.client.force_authenticate(user=self.user)
        
    
    def test_list_user_success(self):
        """
        Test success listing all users
        """
        url = reverse('user-list')
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        response = self.client.get(url)
        users = UserSerializer([self.user], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['results'], users)
        self.assertEqual(response.data['data']['total_count'], len(users))
    
    
    def test_get_user_list_failure(self):
        """
        Test failure listing all users
        """
        self.client.logout()
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        
    def test_retrieve_user_success(self):
        """
        Test success retrieving a user
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('user-detail', args=[self.user.pk])
        response = self.client.get(url)
        category = UserSerializer(self.user).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], category)
        
    
    def test_update_user_success(self):
        """
        Test success updating a user
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('user-detail', args=[self.user.pk])
        data = {
            'name': 'Taco',
            'email': 'Taco@mail.com',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Taco')
    
    
    def test_partial_update_user_success(self):
        """
        Test success partially updating a user
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('user-detail', args=[self.user.pk])
        data = {
            'name': 'Mr. Test',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Mr. Test')
    
    
    def test_delete_user_success(self):
        """
        Test success deleting(deactivating) a user
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('user-detail', args=[self.user.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(id=self.user.pk).exists(), True)
        self.assertEqual(User.objects.get(id=self.user.pk).is_active, False)




class CategoryViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@mail.com",
            password="@Test2024.",
            name="Test"
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(
            name='Shoes and Clothings',
            description='All wearable fashion products'
        )
        self.product = Product.objects.create(
            name='Cussons Baby oil',
            description='For babies and toddlers',
            price=5.99,
            category = self.category,
            quantity=23
        )
        
    
    def test_categories_list_success(self):
        """
        Test success listing all categories
        """
        url = reverse('category-list')
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        response = self.client.get(url)
        categories = CategorySerializer([self.category], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['results'], categories)
        self.assertEqual(response.data['data']['results'][0]['products'][0]['id'], self.product.pk)
        self.assertEqual(response.data['data']['total_count'], len(categories))
    
    
    def test_get_categories_list_unautheneticated_failure(self):
        """
        Test failure listing all categories
        """
        self.client.logout()
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_create_category_success(self):
        """
        Test success creating a category
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('category-list')
        data = {
            'name': 'Gadgets and Devices',
            'description': 'Mobile electronics'
        }
        response = self.client.post(url, data) 
        category = Category.objects.get(name=data['name'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['id'], category.pk)
   
        
    def test_retrieve_category_success(self):
        """
        Test success retrieving a category
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('category-detail', args=[self.category.pk])
        response = self.client.get(url)
        category = CategorySerializer(self.category).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], category)
        
    
    def test_update_category_success(self):
        """
        Test success updating a category
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('category-detail', args=[self.category.pk])
        data = {
            'name': 'Jewelries',
            'description': 'All tinkets and blings'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Jewelries')
    
    
    def test_partial_update_category_success(self):
        """
        Test success partially updating a category
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('category-detail', args=[self.category.pk])
        data = {
            'name': 'Vehicles and Machinery',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Vehicles and Machinery')
        
        
    def test_delete_category_success(self):
        """
        Test success deleting a category
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('category-detail', args=[self.category.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.filter(id=self.category.pk).exists(), False)



class ProductViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@mail.com",
            password="@Test2024.",
            name="Test"
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(
            name='Shoes and Clothings',
            description='All wearable fashion products'
        )
        self.product = Product.objects.create(
            name='Cussons Baby oil',
            description='For babies and toddlers',
            price=5.99,
            category = self.category,
            quantity=23
        )
        
    
    def test_product_list_success(self):
        """
        Test success listing all products
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('product-list')
        response = self.client.get(url)
        products = ProductSerializer([self.product], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['results'], products)
        self.assertEqual(response.data['data']['total_count'], len(products))
    
    
    def test_get_product_list_unautheneticated_failure(self):
        """
        Test failure listing all products
        """
        self.client.logout()
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_create_product_success(self):
        """
        Test success creating a product
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('product-list')
        data = {
            'name': 'Mr. Pearson',
            'description': 'Cereals for kids aged 5-7',
            'price': 2.99,
            'category': self.category.pk,
            'quantity': 2
        }
        response = self.client.post(url, data) 
        product = Product.objects.get(name=data['name'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['id'], product.pk)
        
    def test_retrieve_product_success(self):
        """
        Test success retrieving a product
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('product-detail', args=[self.product.pk])
        response = self.client.get(url)
        product = ProductSerializer(self.product).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], product)

    
    def test_update_product_success(self):
        """
        Test success updating a product
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('product-detail', args=[self.product.pk])
        data = {
            'name': 'Oreos',
            'description': 'Chocolate cookies',
            'price': 2.59,
            'category': self.category.pk,
            'quantity': 88
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Oreos')
    
    
    def test_partial_update_product_success(self):
        """
        Test success partially updating a product
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('product-detail', args=[self.product.pk])
        data = {
            'name': 'Cold stone creamy',
            'description': 'Ice cream for kids',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Cold stone creamy')
        
    
    def test_delete_product_success(self):
        """
        Test success deleting a product
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('product-detail', args=[self.product.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.filter(id=self.product.pk).exists(), False)




class OrderViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@mail.com",
            password="@Test2024.",
            name="Test"
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(
            name='Shoes and Clothings',
            description='All wearable fashion products'
        )
        self.product = Product.objects.create(
            name='Cussons Baby oil',
            description='For babies and toddlers',
            price=5.99,
            category = self.category,
            quantity=23
        )
        self.order = Order.objects.create(user=self.user)
        self.order.products.add(self.product.pk)
        
    
    def test_user_order_list_success(self):
        """
        Test success listing user's orders
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('order-list')
        response = self.client.get(url)
        orders = OrderSerializer([self.order], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['results'], orders)
        self.assertEqual(response.data['data']['total_count'], len(orders))
    
    
    def test_get_categories_list_unautheneticated_failure(self):
        """
        Test failure listing user's orders
        """
        self.client.logout()
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_create_order_success(self):
        """
        Test success creating user's order
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('order-list')
        data = {
            'user': self.user.pk,
            'products': [
                self.product.pk,
            ],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['user'], self.user.pk)
        
        
    def test_retrieve_order_success(self):
        """
        Test success retrieving user's order
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('order-detail', args=[self.order.pk])
        response = self.client.get(url)
        order = OrderSerializer(self.order).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], order)

    
    def test_update_order_success(self):
        """
        Test success updating user's order
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('product-list')
        data = {
            'name': 'Oreos',
            'description': 'Chocolate cookies',
            'price': 2.59,
            'category': self.category.pk,
            'quantity': 88
        }
        new_product = self.client.post(url, data)
        
        url = reverse('order-detail', args=[self.order.pk])
        data = {
            'user': self.user.pk,
            'products': [
                self.product.pk,
                new_product.data['data']['id']
            ],
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['products']), 2)
    
    
    def test_partial_update_order_success(self):
        """
        Test success partially updating user's order
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('product-list')
        data = {
            'name': 'Oreos',
            'description': 'Chocolate cookies',
            'price': 2.59,
            'category': self.category.pk,
            'quantity': 88
        }
        new_product = self.client.post(url, data)
        
        url = reverse('order-detail', args=[self.order.pk])
        data = {
            'products': [
                self.product.pk,
                new_product.data['data']['id']
            ],
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['products']), 2)
        
    
    def test_delete_order_success(self):
        """
        Test success deleting user's order
        """
        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + self.user.get_tokens()['access'])
        url = reverse('order-detail', args=[self.order.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.filter(id=self.order.pk).exists(), False)