from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework_simplejwt import views, serializers
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import User, Task
from .serializers import RegisterSerializer, TaskSerializer


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        responses={
            '201': openapi.Response(
                description='Created',
                examples={
                    'application/json': {
                        'username': 'string',
                        'email': 'user@example.com',
                    },
                },
                schema=RegisterSerializer,
            ),
            '400': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'username': [
                            'A user with that username already exists.',
                        ],
                        'email': [
                            'A user with this email already exist',
                        ],
                    },
                },
                schema=RegisterSerializer,
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

      
class TaskViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.ListModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        responses={
            '201': openapi.Response(
                description='Created',
                examples={
                    'application/json': {
                        'id': 1,
                        'title': "Hello",
                        'description': 0,
                        'start_date': "2022-06-30T00:00:00Z",
                        'end_date': "2023-07-30T20:30:00Z",
                        'user': 1
                    },
                },
                schema=TaskSerializer,
            ),
            '400': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'title': [
                            "This field is required."
                        ],
                        'start_date': [
                            "This field is required."
                        ],
                        'end_date': [
                            "This field is required."
                        ]
                    },
                },
                schema=TaskSerializer,
            ),
            '401': openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail': "Authentication credentials were not provided."
                    },
                },
                schema=TaskSerializer,
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedToSwaggerTokenRefreshView(views.TokenRefreshView):

    @swagger_auto_schema(
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': {
                        'access': 'string',
                        'refresh': 'string',
                    },
                },
                schema=serializers.TokenRefreshSerializer,
            ),
            '400': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'refresh': ['This field may not be blank.',],
                    },
                },
                schema=serializers.TokenRefreshSerializer,
            ),
            '401': openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        "detail": "Token is invalid or expired",
                        "code": "token_not_valid",
                    },
                },
                schema=serializers.TokenRefreshSerializer,
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
