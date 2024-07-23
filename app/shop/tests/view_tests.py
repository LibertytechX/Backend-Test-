from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from shop.models import Product, Category, Order, OrderItem

User = get_user_model()


class BaseViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            email='admin@test.com', password='password123')

        self.normal_user = User.objects.create_user(
            email='user@test.com', password='password123')

        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='A product for testing',
            category=self.category,
            price=100,
            stock=10,
            is_available=True
        )

        self.order = Order.objects.create(user=self.normal_user)
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1)

    def authenticate(self, user):
        self.client.force_authenticate(user=user)


class ProductViewSetTest(BaseViewSetTest):
    def test_list_products(self):
        response = self.client.get('/product/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_products(self):
        response = self.client.get('/product/', {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_product_as_admin(self):
        self.authenticate(self.admin_user)
        data = {
            'category': self.category.id,
            'name': 'New Product',
            'description': 'A new product',
            'price': 200,
            'stock': 20,
        }
        response = self.client.post('/product/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_as_user(self):
        self.authenticate(self.normal_user)
        data = {
            'name': 'New Product',
            'description': 'A new product',
            'category': self.category.id,
            'price': 200,
            'stock': 20,
            'is_available': True
        }
        response = self.client.post('/product/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_product(self):
        response = self.client.get(f'/product/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_update_product(self):
        self.authenticate(self.admin_user)
        data = {
            'name': 'Updated Product',
            'description': 'Updated description',
            'category': self.category.id,
            'price': 150,
            'stock': 5,
        }
        response = self.client.put(f'/product/{self.product.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_delete_product(self):
        self.authenticate(self.admin_user)
        response = self.client.delete(f'/product/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())


class CategoryViewSetTest(BaseViewSetTest):
    def test_list_categories(self):
        response = self.client.get('/category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_categories(self):
        response = self.client.get('/category/', {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_category_as_admin(self):
        self.authenticate(self.admin_user)
        data = {
            'name': 'New Category'
        }
        response = self.client.post('/category/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_as_user(self):
        self.authenticate(self.normal_user)
        data = {
            'name': 'New Category'
        }
        response = self.client.post('/category/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_category(self):
        response = self.client.get(f'/category/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Category')

    def test_update_category(self):
        self.authenticate(self.admin_user)
        data = {
            'name': 'Updated Category'
        }
        response = self.client.put(f'/category/{self.category.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_delete_category(self):
        self.authenticate(self.admin_user)
        response = self.client.delete(f'/category/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())


class OrderItemViewSetTest(BaseViewSetTest):
    def test_list_order_items(self):
        self.authenticate(self.normal_user)
        response = self.client.get('/orderitem/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_order_item(self):
        self.authenticate(self.normal_user)
        response = self.client.get(f'/orderitem/{self.order_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 1)

    def test_update_order_item(self):
        self.authenticate(self.normal_user)
        data = {
            'order': self.order.id,
            'product': self.product.id,
            'quantity': 2
        }
        response = self.client.put(f'/orderitem/{self.order_item.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.quantity, 2)

    def test_delete_order_item(self):
        self.authenticate(self.normal_user)
        response = self.client.delete(f'/orderitem/{self.order_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(OrderItem.objects.filter(
            id=self.order_item.id).exists())


class OrderViewSetTest(BaseViewSetTest):
    def test_list_orders(self):
        self.authenticate(self.normal_user)
        response = self.client.get('/order/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_order(self):
        self.authenticate(self.normal_user)
        data = {
            "user": self.normal_user,
            "order_items": self.order_item,
        }
        response = self.client.post('/order/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_order(self):
        self.authenticate(self.normal_user)
        response = self.client.get(f'/order/{self.order.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order.id)

    def test_update_order(self):
        self.authenticate(self.admin_user)
        data = {}
        response = self.client.put(f'/order/{self.order.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order_as_admin(self):
        self.authenticate(self.admin_user)
        response = self.client.delete(f'/order/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_delete_order_as_owner(self):
        self.authenticate(self.normal_user)
        response = self.client.delete(f'/order/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_delete_order_as_other_user(self):
        other_user = User.objects.create_user(
            'other_user@test.com', 'password123')
        self.authenticate(other_user)
        response = self.client.delete(f'/order/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
