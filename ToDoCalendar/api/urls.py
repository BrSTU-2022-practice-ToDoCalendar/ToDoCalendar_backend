from django.urls import include, path
from .views import MyCustomViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'register', MyCustomViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]