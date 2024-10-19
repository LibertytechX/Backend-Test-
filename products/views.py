from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Q
from products.models import Product
from products.serializers import ProductSerializer, CreateProductSerializer
from utils.response import service_response
from utils.exceptions import handle_internal_server_exception
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import MethodNotAllowed

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    """Product REST Viewset"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        """List all products"""
        try:
            # TODO: Implement search for products
            search_query = request.query_params.get("search", None)
            category = request.query_params.get("category", None)
            if search_query:
                products = Product.objects.filter(
                    Q(name__icontains=search_query)
                    | Q(description__icontains=search_query)
                )
            # TODO: Filter by category
            elif category:
                products = Product.objects.filter(category=int(category))
            else:
                products = Product.objects.all()
            # TODO: Implement pagination

            paginator = Paginator(products, 30)
            page = request.query_params.get("page", 1)
            try:
                products_page = paginator.page(page)
            except PageNotAnInteger:
                products_page = paginator.page(1)
            except EmptyPage:
                products_page = paginator.page(paginator.num_pages)

            total_pages = paginator.num_pages
            serialized_products = self.get_serializer(products_page, many=True)
            data = {
                "products": serialized_products.data,
                "total_pages": total_pages,
                "current_page": int(page),
            }
            return service_response(
                status="success", data=data, message="Fetch Successful", status_code=200
            )
        except Exception:
            return handle_internal_server_exception()

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single product"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return service_response(
                status="success",
                data=serializer.data,
                message="Fetch Successful",
                status_code=200,
            )
        except Exception:
            return handle_internal_server_exception()

    def create(self, request, *args, **kwargs):
        """Create a new product"""
        try:
            serializer = CreateProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return service_response(
                    status="success",
                    data=serializer.data,
                    message="Product created successfully",
                    status_code=201,
                )
            return service_response(
                status="error", message=serializer.errors, status_code=400
            )
        except Exception:
            return handle_internal_server_exception()

    def get_permissions(self):
        # TODO: remove the create from this
        unsecure_actions = ["list", "retrieve", "create", "update", "destroy"]
        if self.action in unsecure_actions:
            return [AllowAny()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        """Update an existing product"""
        try:
            instance = self.get_object()
            serializer = CreateProductSerializer(instance=instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return service_response(
                    status="success",
                    data=serializer.data,
                    message="Product updated successfully",
                    status_code=200,
                )
            return service_response(
                status="error", message=serializer.errors, status_code=400
            )
        except Exception:
            return handle_internal_server_exception()

    def destroy(self, request, *args, **kwargs):
        """Delete an existing product"""
        try:
            instance = self.get_object()
            instance.delete()
            return service_response(
                status="success",
                data=None,
                message="Product deleted successfully",
                status_code=204,
            )
        except Exception:
            return handle_internal_server_exception()

    # restrict patch method
    def patch(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
