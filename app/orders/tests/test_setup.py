from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from faker import Faker
from products.models import ProductCategory, Product


class OrderTestsSetUp(APITestCase):

    def setUp(self):
        """ Handles set up of test variables and env for Order. """
        self.faker = Faker()
        self.email = self.faker.email()
        self.product_data_one = {
            'name': self.faker.name(),
            'description': self.faker.text(max_nb_chars=100),
            'price': self.faker.numerify('##.##'),
        }
        self.product_data_two = {
            'name': self.faker.name(),
            'description': self.faker.text(max_nb_chars=100),
            'price': self.faker.numerify('##.##'),
        }
        # Create model instances to boot test
        self.category = ProductCategory.objects.create(name='Electronics')
        self.product_one = Product.objects.create(category=self.category,
                                                  **self.product_data_one)
        self.product_two = Product.objects.create(category=self.category,
                                                  **self.product_data_two)
        self.user = get_user_model().objects.create_user(
            email=self.email, password=self.faker.password())

        self.token = AccessToken.for_user(self.user)
        self.order_list_url = reverse('orders-list')

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
