from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from faker import Faker
from ..models import ProductCategory, Product


class ProductTestsSetUp(APITestCase):

    def setUp(self):
        """ Handles set up of test variables and env for Product. """
        self.faker = Faker()
        self.product_data = {
            'name': self.faker.name(),
            'description': self.faker.text(max_nb_chars=100),
            'price': self.faker.numerify('##.##'),
        }
        self.category = ProductCategory.objects.create(name='Electronics')
        self.product = Product.objects.create(**self.product_data,
                                              category=self.category)
        self.user = get_user_model().objects.create_user(
            email=self.faker.email(), password=self.faker.password())
        self.token = AccessToken.for_user(self.user)

        self.product_list_url = reverse('products-list')
        self.product_detail_url = reverse('products-detail',
                                          args=(self.product.id, ))

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
