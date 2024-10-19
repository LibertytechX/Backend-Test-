from ninja import Schema, ModelSchema, Form
from core.models import User, Category, Order
from datetime import datetime



class UserSchema(ModelSchema):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ["password", "user_permissions"]


# class LoginSchema(Schema):
#     username: Form[str]
#     password: Form[str]

class SignUpSchema(Schema):
    username: str
    first_name: str
    last_name: str
    role: str
    email: str
    phone_no: str
    created_at: datetime
    password: str


class NotFoundError(Schema):
    message: str



class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        fields = "__all__"


class CreateCategorySchema(Schema):
    title: str
    created_at: datetime



class ProductSchema(Schema):
    category: CategorySchema
    name: str
    description: str
    price: float
    creator: UserSchema
    created_at: datetime



class OrderSchema(Schema):
    buyer: UserSchema
    seller: UserSchema
    item: ProductSchema
    paid: bool
    order_no: str
    delivered: bool
    completed: bool
    created_at: datetime


class CreateProductSchema(Schema):
    name: str = Form(...)
    description: str = Form(...)
    price: int = Form(...)
    created_at: datetime


# class CreateOrderSchema(Schema):
#     delivered: bool