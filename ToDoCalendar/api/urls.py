from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import RegisterViewSet, TaskViewSet


router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'task', TaskViewSet, basename='task')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/refresh-token/', TokenRefreshView.as_view()),
    path('v1/verify-token/', TokenVerifyView.as_view()),
]
