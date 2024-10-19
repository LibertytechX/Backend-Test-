from django.http import HttpRequest
from ninja import Query
from ninja_extra import (
    NinjaExtraAPI, api_controller, http_delete, http_get, http_post, http_put, route, pagination, status,
    ControllerBase
)
from ninja.security import HttpBearer
from ninja.constants import NOT_SET

from .models import (
    User, Order, Category, Product
)
from django.contrib.auth import authenticate, login, logout
from ninja.errors import HttpError

from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth

from .api_schema.schema import(
    UserSchema, NotFoundError, CategorySchema, OrderSchema, CreateCategorySchema,
    ProductSchema, CreateProductSchema, SignUpSchema
) 

from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth.hashers import make_password
# from . import search



        

api = NinjaExtraAPI(title="InventoryApi", description="Products")


@api_controller("/users", tags=["Users"], permissions=[], auth=JWTAuth())
class UserPath:
   
    @route.get("/", response=list[UserSchema])
    def get_users(self, request):
        print(request.user.id)
        return User.objects.all()


    @route.get("/user", response={200: UserSchema, 404: NotFoundError})
    def get_user(self, request):
        user = request.user
        try:
            user = User.objects.get(id=user.id)
            return user
        except User.DoesNotExist as e:
            return 404, {"message": "User not found"}
        



@api_controller("/registration", tags=["Register"])
class Register:
    @route.post("", response={200: UserSchema, 404: NotFoundError})
    def register(self, payload: SignUpSchema):
        try:
            user = User.objects.create(
                username=payload.username,
                first_name=payload.first_name,
                last_name=payload.last_name,
                role=payload.role,
                email=payload.email,
                phone_no=payload.phone_no,
                password=make_password(payload.password)
            )
            return user
        except Category.DoesNotExist as e:
            return 404, {"message": "error creating user"}



@api_controller("/inventory", tags=["inventory"])
class Inventory:

    @route.get("/category", response={200: list[CategorySchema], 404: NotFoundError})
    def get_category(self, request):
        user = request.user
        try:
            category = Category.objects.all()
            return category
        except Category.DoesNotExist as e:
            return 404, {"message": "User not found"}
    
    
    @route.post("/category", response={200: CategorySchema, 404: NotFoundError})
    def create_category(self, request, payload: CreateCategorySchema):
        user = request.user
        try:
            category = Category.objects.create(
                title = payload.title
            )
            return category
        except Category.DoesNotExist as e:
            return 404, {"message": "User not found"}
        

    @route.get("/product", response={200: ProductSchema, 404: NotFoundError}, auth=JWTAuth())
    def get_product(self, request):
        user = request.user
        try:
            product = Product.objects.all()
            return product
        except Product.DoesNotExist as e:
            return 404, {"message": "User not found"}
        



#### Product Crud  APIs #
@api_controller("/product", tags=["Product"])
class Products:

    @http_get("", response={200: pagination.PaginatedResponseSchema[ProductSchema], 401: NotFoundError})
    @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=10)
    def get_product_per_creator(self, creator_id: int | None = None):
        if not creator_id:
            try:
                product = Product.objects.all()
                return product
            except Product.DoesNotExist as e:
                return 401, {"message": "No Products found"}
        else:
            try:
                creator = User.objects.get(id=creator_id)
                product = Product.objects.filter(author=creator)
                return product
            except Product.DoesNotExist as err:
                return 401, {"message": "Nothing to see here"}
                
    
    
    @http_get("/get", response={200: pagination.PaginatedResponseSchema[ProductSchema], 401: NotFoundError})
    @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=10)
    def get_product(self):
        try:
            product = Product.objects.all()
            return product
        except Product.DoesNotExist as e:
            return 401, {"message": "No products found"}


    @http_post("/create_product", response={200: ProductSchema, 401: NotFoundError}, auth=JWTAuth())
    def create_product(self, request, category_id: int, payload: CreateProductSchema):
        user = request.user
        try:
            category = Category.objects.get(id=category_id)
            product = Product.objects.create(
                name=payload.name,
                description=payload.description,
                price=payload.price,
                creator=user,
                category=category
            )
            return product
        except Category.DoesNotExist as e:
            return 401, {"message": "This is not a category"}
    
    
    @http_put("/updated_product", response={200: ProductSchema, 401: NotFoundError}, auth=JWTAuth())
    def update_product(self, request, product_id: int, payload: CreateProductSchema):
        user = request.user
        print(type(user))
        try:
            product = Product.objects.get(id=product_id)
    
            product.name=payload.name
            product.description=payload.description
            product.price=payload.price
            product.save()
            return product
        
        except Product.DoesNotExist:
            return 401, {"message": "Product Not found"}
        
        
    @http_delete("/delete", auth=JWTAuth())
    def delete_product(self, product_id: int):
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return {"message": "Product deleted"}
        except Product.DoesNotExist as err:
            return {"message": "Nothing to delete here"}
        


@api_controller("/order", tags=["Order"])
class Orders:

    @http_post("/create", auth=JWTAuth(), response={200: list[OrderSchema], 401: NotFoundError})
    def create_order(self, request, item_ids: list[int]):
        buyer = request.user
        created_orders = []
        errors = []
        for item_id in item_ids:
            
            try:
                item = Product.objects.get(pk=item_id)
                order = Order.objects.create(
                    buyer=buyer,
                    seller=item.creator,
                    item=item
                )
                created_orders.append(order)
            except Product.DoesNotExist:
                errors.append({"item_id": item_id, "message": "Product not found"})
            except Exception as e:
                errors.append({"item_id": item_id, "message": str(e)})
        if not created_orders:
            return 401, {"message": "No orders created", "errors": errors}
        
        return created_orders
        


    @http_get("/", auth=JWTAuth(), response={200: pagination.PaginatedResponseSchema[OrderSchema], 404: NotFoundError})
    @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=10)
    def get_orders(self, request):
        buyer = request.user
        if buyer.is_authenticated:
            try:
                order = Order.objects.filter(buyer=buyer).order_by("-created_at")
                return order
            except Order.DoesNotExist as e:
                return 400, {"message": "No orders found"}
        
    


api.register_controllers(
    Register,
    UserPath,
    NinjaJWTDefaultController,
    Inventory,
    Products,
    Orders,
)




