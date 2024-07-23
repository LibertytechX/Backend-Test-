from django.test import TestCase
from shop.exceptions import OutOfStocksException
from shop.models import Category, Product, OrderItem, Order
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

    def test_string_representation(self):
        self.assertEqual(str(self.category), f"Category: {self.category.name}")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            description="A powerful laptop",
            category=self.category,
            price=150000,
            stock=10,
            is_available=True,
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.product), f"Product: {self.product.name} (NGN {self.product.price})")

    def test_check_product_inventory(self):
        self.product.stock = 0
        self.product.check_product_inventory()
        self.assertFalse(self.product.is_available)

        self.product.stock = 5
        self.product.check_product_inventory()
        self.assertTrue(self.product.is_available)

    def test_save_method(self):
        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.is_available)


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@email.com", password="testpass")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            description="A powerful laptop",
            category=self.category,
            price=150000,
            stock=10,
            is_available=True,
        )
        self.order = Order.objects.create(user=self.user)

    def test_string_representation(self):
        order_item = OrderItem.objects.create(
            product=self.product, quantity=1, order=self.order)
        self.assertEqual(
            str(order_item), f"Ordered {order_item.quantity} of {order_item.product}")

    def test_save_method(self):
        order_item = OrderItem(product=self.product,
                               quantity=5, order=self.order)
        order_item.save()
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)

        with self.assertRaises(OutOfStocksException):
            order_item = OrderItem(product=self.product,
                                   quantity=6, order=self.order)
            order_item.save()

    def test_delete_method(self):
        order_item = OrderItem.objects.create(
            product=self.product, quantity=5, order=self.order)
        initial_stock = self.product.stock
        order_item.delete()
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock + 5)


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@email.com", password="testpass")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            description="A powerful laptop",
            category=self.category,
            price=150000,
            stock=10,
            is_available=True,
        )
        self.order = Order.objects.create(user=self.user)

    def test_string_representation(self):
        self.assertEqual(str(self.order), f"Order by {self.user.name}")

    def test_order_item_relationship(self):
        order_item = OrderItem.objects.create(
            product=self.product, quantity=2, order=self.order)
        self.order.products.add(self.product, through_defaults={'quantity': 2})
        self.assertIn(order_item, self.order.orderitem_set.all())
