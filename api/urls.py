from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterViewSet,
    TaskViewSet,
    DecoratedToSwaggerTokenRefreshView,
    DecoratedToSwaggerTokenObtainPairView,
    DecoratedToSwaggerTokenVerifyView
)


router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'task', TaskViewSet, basename='task')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/login/', DecoratedToSwaggerTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/refresh-token/', DecoratedToSwaggerTokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/verify-token/', DecoratedToSwaggerTokenVerifyView.as_view(),
         name='token_verify'),
]
