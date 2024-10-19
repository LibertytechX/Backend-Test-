from django.test import TestCase
from rest_framework.test import APIClient
from products.models import Product, Category
from django.core.paginator import Paginator


class ProductViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_url = "/api/v1/products"
        # Create 60 products for testing pagination
        for i in range(60):
            Product.objects.create(
                name=f"Product {i}", description="Test product", price=10.0
            )

    def test_pagination_first_page(self):
        response = self.client.get(f"{self.base_url}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["data"]["products"]), 30)
        self.assertEqual(data["data"]["total_pages"], 2)
        self.assertEqual(data["data"]["current_page"], 1)

    def test_pagination_second_page(self):
        response = self.client.get(f"{self.base_url}?page=2")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["data"]["products"]), 30)
        self.assertEqual(data["data"]["total_pages"], 2)
        self.assertEqual(data["data"]["current_page"], 2)

    def test_pagination_no_page_param(self):
        response = self.client.get(f"{self.base_url}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["data"]["products"]), 30)
        self.assertEqual(data["data"]["total_pages"], 2)
        self.assertEqual(data["data"]["current_page"], 1)

    def test_create_product_returns_201(self):
        # create category
        cat = Category.objects.create(name="Test Category")
        data = {
            "category": cat.id,
            "name": "Iphone test 12",
            "available_quantity": 20,
            "price": 2000000,
            "discount_price": 190000,
            "description": "some description",
        }
        response = self.client.post(f"{self.base_url}", data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_product_returns_200(self):
        cat = Category.objects.create(name="Test Category")
        product = Product.objects.create(
            category=cat,
            name="Iphone 12",
            available_quantity=20,
            price=2000000,
            discount_price=190000,
            description="some description",
        )
        data = {
            "category": cat.id,
            "name": "Iphone 12",
            "available_quantity": 20,
            "price": 2300000,
            "discount_price": 2000000,
            "description": "some description updated",
        }
        response = self.client.put(f"{self.base_url}/{product.id}", data, format="json")
        self.assertEqual(response.status_code, 200)
        assert "some description updated" in response.json()["data"]["description"]

    def test_retrieve_products_returns_200(self):
        cat = Category.objects.create(name="Test Category")
        product = Product.objects.create(
            category=cat,
            name="Iphone 12",
            available_quantity=20,
            price=2000000,
            discount_price=190000,
            description="some description",
        )
        response = self.client.get(f"{self.base_url}/{product.id}")
        self.assertEqual(response.status_code, 200)
        assert product.name == response.json()["data"]["name"]

    def test_delete_product_returns_204(self):
        cat = Category.objects.create(name="Test Category")
        product = Product.objects.create(
            category=cat,
            name="Iphone 12",
            available_quantity=20,
            price=2000000,
            discount_price=190000,
            description="some description",
        )
        response = self.client.delete(f"{self.base_url}/{product.id}")
        self.assertEqual(response.status_code, 204)
        assert not Product.objects.filter(pk=product.id).exists()
