import re
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from django.core.validators import DecimalValidator
from product.models import Product, Category

class ProductDataValidator:
    def __init__(self, data):
        self.data = data
        self.errors = {}

    def validate(self):
        self._validate_name()
        self._validate_description()
        self._validate_price()
        self._validate_stock()
        self._validate_sku()
        self._validate_category()
        return self.errors

    def _validate_name(self):
        name = self.data.get('name')
        if not name:
            self.errors['name'] = "Product name is required."
        elif len(name) < 3:
            self.errors['name'] = "Product name must be at least 3 characters long."

    def _validate_description(self):
        description = self.data.get('description')
        if not description:
            self.errors['description'] = "Product description is required."
        elif len(description) < 10:
            self.errors['description'] = "Product description must be at least 10 characters long."

    def _validate_price(self):
        price = self.data.get('price')
        if not price:
            self.errors['price'] = "Product price is required."
            return

        try:
            price = Decimal(price)
        except InvalidOperation:
            self.errors['price'] = "Please enter a valid price."
            return

        decimal_validator = DecimalValidator(max_digits=10, decimal_places=2)
        try:
            decimal_validator(price)
        except ValidationError:
            self.errors['price'] = "Please enter a valid price (up to 2 decimal places)."
            return

        if price <= 0:
            self.errors['price'] = "Product price must be greater than 0."

    def _validate_stock(self):
        stock = self.data.get('stock')
        if stock is None:
            self.errors['stock'] = "Product stock is required."
        elif not isinstance(stock, int) or stock < 0:
            self.errors['stock'] = "Product stock must be a non-negative integer."

    def _validate_sku(self):
        sku = self.data.get('sku')
        if not sku:
            self.errors['sku'] = "Product SKU is required."
        elif len(sku) < 5:
            self.errors['sku'] = "Product SKU must be at least 5 characters long."
        elif not re.match(r'^[A-Z0-9]+$', sku):
            self.errors['sku'] = "Product SKU must contain only uppercase letters and numbers."

    def _validate_category(self):
        category_id = self.data.get('category')
        if not category_id:
            self.errors['category'] = "Product category is required."
        elif not Category.objects.filter(id=category_id).exists():
            self.errors['category'] = f"Category with id {category_id} does not exist."

class OrderDataValidator:
    def __init__(self, data):
        self.data = data
        self.errors = {}

    def validate(self):
        self._validate_products()
        return self.errors

    def _validate_products(self):
        products = self.data.get('products')
        if not products or len(products) == 0:
            self.errors['products'] = "Order must contain at least one product."
            return

        for item in products:
            product_id = item.get('product')
            quantity = item.get('quantity')
            price = item.get('price')

            if not product_id:
                self.errors['product'] = "Product ID is required for each item."
                continue

            if not Product.objects.filter(id=product_id).exists():
                self.errors['product'] = f"Product with id {product_id} does not exist."
            
            if not quantity:
                self.errors['quantity'] = "Quantity is required for each item."
            elif not isinstance(quantity, int) or quantity <= 0:
                self.errors['quantity'] = "Quantity must be a positive integer."

            if not price:
                self.errors['price'] = "Price is required for each item."
                continue

            try:
                price = Decimal(price)
            except InvalidOperation:
                self.errors['price'] = "Please enter a valid price."
                continue

            decimal_validator = DecimalValidator(max_digits=10, decimal_places=2)
            try:
                decimal_validator(price)
            except ValidationError:
                self.errors['price'] = "Please enter a valid price (up to 2 decimal places)."
                continue

            if price <= 0:
                self.errors['price'] = "Product price must be greater than 0."

def validate_product_data(data):
    validator = ProductDataValidator(data)
    return validator.validate()

def validate_order_data(data):
    validator = OrderDataValidator(data)
    return validator.validate()