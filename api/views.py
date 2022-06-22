from rest_framework import mixins
from rest_framework import viewsets

from .models import User
from .models import Task
from .serializers import RegisterSerializer
from .serializers import TaskSerializer


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class TaskViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
