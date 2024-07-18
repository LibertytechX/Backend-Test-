from django.http import JsonResponse
from django.urls import path
from core import views


def homepage(request):
    return JsonResponse({"message": "Liberty Test APIs (Backend)"})


app_name = "core"


urlpatterns = [
    path('', homepage),
    path('signup', views.SignUpAPIView.as_view(), name="signup"),
    path('login', views.LoginAPIView.as_view(), name="login"),
    path('product-category', views.ProductCategoryListCreateAPIView.as_view(), name="product-category"),
    path('product', views.ProductCreateUpdateDeleteAPIView.as_view(), name="product"),
    path('product/<int:pk>', views.ProductCreateUpdateDeleteAPIView.as_view(), name="product-update-delete"),
    path('product-list', views.ProductListAPIView.as_view(), name="product-listing"),
    path('order', views.OrderPlacementAPIView.as_view(), name="order"),

]
