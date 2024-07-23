from django.urls import path
from .views import LoginAPIView, UserViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user', UserViewSet, "user")

urlpatterns = router.urls
urlpatterns += [
    path('login/', LoginAPIView.as_view(), name='login'),
]
