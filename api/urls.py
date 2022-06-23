from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from .views import RegisterViewSet

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/login/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/login/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/login/verify/', jwt_views.TokenVerifyView.as_view(),
         name='token_verify'),
]
