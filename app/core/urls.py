from rest_framework.routers import SimpleRouter

from core.views.auth_view import AuthViewSet
from core.views.user_view import UserViewSet
from core.views.category_view import CategoryViewSet
from core.views.product_view import ProductViewSet
from core.views.order_view import OrderViewSet

auth_router = SimpleRouter()
users_router = SimpleRouter()
category_router = SimpleRouter()
product_router = SimpleRouter()
order_router = SimpleRouter()

auth_router.register(r'auth', AuthViewSet)
users_router.register(r'users', UserViewSet)
category_router.register(r'categories', CategoryViewSet)
product_router.register(r'products', ProductViewSet)
order_router.register(r'orders', OrderViewSet)  