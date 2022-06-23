from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import User
from .models import Task
from .serializers import RegisterSerializer
from .serializers import TaskSerializer


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class TaskViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.ListModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_user_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def custom_create(self, serializer):
        serializer.save(user=self.request.user)
