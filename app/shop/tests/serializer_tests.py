from rest_framework.test import APIClient, APIRequestFactory
from django.test import TestCase
from core.models import User
from shop.models import Category, Order, OrderItem, Product
from shop.serializers import CategorySerializer, OrderSerializer, OrderItemSerializer, ProductSerializer


class BaseTest(TestCase):
    def setUp(self):
        user_email = "test@email.com"
        self.user = User.objects.create_user(
            email=user_email, password="testpassword")

        self.order = Order.objects.create(user=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='A product for testing',
            category=self.category,
            price=100,
            stock=10,
            is_available=True
        )

        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1)


class TestOrderItemSerializer(BaseTest):

    def test_serialize(self):
        serializer = OrderItemSerializer(self.order_item)
        data = serializer.data
        self.assertEqual(set(data.keys()), {
                         'id', 'order', 'product', 'quantity'})
        self.assertEqual(data['quantity'], 1)

    def test_deserialize(self):
        data = {'order': self.order_item.order.pk,
                'product': self.order_item.product.pk, 'quantity': 2}
        serializer = OrderItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(OrderItem.objects.count(), 2)


class TestOrderSerializer(BaseTest):

    def test_serialize(self):
        serializer = OrderSerializer(self.order)
        data = serializer.data
        self.assertEqual(set(data.keys()), {
                         'id', 'products', 'is_checked_out', 'created_at', 'updated_at'})


class TestProductSerializer(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product', price=100, stock=10, category=self.category)

        client = APIRequestFactory()
        self.context = {"request": client.request}

    def test_deserialize(self):
        data = {'category': self.category.pk, 'name': 'New Product',
                'price': 200, 'stock': 20, 'description': 'New product description'}
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        serializer.save()
        self.assertEqual(Product.objects.count(), 2)

    def test_deserialize_invalid_data(self):
        data = {'category': self.category.pk, 'name': '', 'price': 200,
                'tock': 20, 'description': 'New product description'}
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertNotEqual(serializer.errors, {})


class TestCategorySerializer(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product', price=100, stock=10, category=self.category)
        self.context = {"request": APIClient().request}

    def test_deserialize(self):
        data = {'name': 'New Category'}
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        serializer.save()
        self.assertEqual(Category.objects.count(), 2)

    def test_deserialize_invalid_data(self):
        data = {'name': ''}
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertNotEqual(serializer.errors, {})
