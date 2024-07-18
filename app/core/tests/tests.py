import json

from django.urls import reverse
from django.test import TestCase
from rest_framework import status

from core.models import User


class TestCoreTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(email="test@email.com", password="Test@123", name="Sunday", is_staff=True)

    def test_valid_signup(self):
        data = {"email": "test1@email.com", "password": "Test@123", "name": "Sunday"}
        url = reverse("core:signup")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_login(self):
        data = {"email": "test@email.com", "password": "Test@123"}
        url = reverse("core:login")
        response = self.client.post(url, data)
        res = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return res["access_token"]

    def test_invalid_login(self):
        data = {"email": "test@email.com", "password": "Testing@123"}
        url = reverse("core:login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_category_list(self):
        header_data = {"Authorization": f"Bearer {self.test_valid_login()}"}
        url = reverse("core:product-category")
        response = self.client.get(url, headers=header_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_category_creation(self):
        header_data = {"Authorization": f"Bearer {self.test_valid_login()}"}
        data = {"name": "Mobile Phone"}
        url = reverse("core:product-category")
        response = self.client.post(url, data, headers=header_data)
        res = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return res["id"]

    def test_product_creation(self):
        header_data = {"Authorization": f"Bearer {self.test_valid_login()}"}
        data = {
            "name": "LG Smart TV", "description": "Smart Television", "price": 3000,
            "category_id": self.test_product_category_creation()
        }
        url = reverse("core:product")
        response = self.client.post(url, data, headers=header_data)
        res = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return res["data"]["id"]

    def test_product_update(self):
        header_data = {"Authorization": f"Bearer {self.test_valid_login()}", "Content-Type": "application/json"}
        data = json.dumps({
            "name": "LG Smart TV (NEW)", "description": "Smart Television", "price": 5000,
            "category_id": self.test_product_category_creation()
        })
        url = reverse("core:product-update-delete", kwargs={'pk': self.test_product_creation()})
        response = self.client.put(url, data, headers=header_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_delete(self):
        header_data = {"Authorization": f"Bearer {self.test_valid_login()}"}
        url = reverse("core:product-update-delete", args=[int(self.test_product_creation())])
        response = self.client.delete(url, headers=header_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list(self):
        header_data = {"Authorization": f"Bearer {self.test_valid_login()}"}
        url = reverse("core:product-listing")
        response = self.client.get(url, headers=header_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_placement(self):
        header_data = {"Authorization": f"Bearer {self.test_valid_login()}"}
        order_request = list()
        order_details = dict()
        order_details["product_id"] = int(self.test_product_creation())
        order_details["quantity"] = 20
        order_request.append(order_details)
        data = dict()
        data["order_request"] = order_request
        url = reverse("core:order")
        response = self.client.post(url, data=data, headers=header_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_list(self):
        header_data = {"Authorization": f"Bearer {self.test_valid_login()}"}
        url = reverse("core:order")
        response = self.client.get(url, headers=header_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
