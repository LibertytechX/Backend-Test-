
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import user_views, product_views, order_views
# from core.views.product_views import CategoryViewSet

router = DefaultRouter()
router.register(r'category', product_views.CategoryViewSet)

urlpatterns = [
    # auth urls
    path('signup/customer', user_views.CustomerRegistrationView.as_view()),
    path('signup/staff', user_views.StaffRegistrationView.as_view()),
    path('login', user_views.MyTokenObtainPairView.as_view()),

    # product url
    path('product/create', product_views.ProductCreateView.as_view(),
         name="create-product"),
    path('product/list', product_views.ProductListView.as_view(), name="product-list"),
    path('product/<int:pk>', product_views.ProductGetDetailView.as_view(),
         name="product-detail"),
    path('product/update_delete/<int:pk>',
         product_views.ProductUpdateDeleteView.as_view(), name="product-update-delete"),


    # order url
    path('order/create', order_views.PlaceOrderView.as_view(), name="create-order"),
    path('order/list', order_views.OrderListView.as_view(), name="order-list"),
    path('order/history', order_views.OrderUserHistoryView.as_view(),
         name="order-user-history"),
    path('order/<int:pk>', order_views.OrderGetView.as_view(), name="order-detail"),

    # category url
    path('', include(router.urls)),

    #  not found route

]
