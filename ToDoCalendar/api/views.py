from rest_framework import mixins
from rest_framework import viewsets

from .models import User
from .serializers import RegisterSerializer


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


