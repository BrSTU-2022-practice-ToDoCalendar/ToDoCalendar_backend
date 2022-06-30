from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
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


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': [{
                        'id': 0,
                        'title': 'string',
                        'description': 'string',
                        'start_date': '2019-08-24T14:15:22Z',
                        'end_date': '2019-08-24T14:15:22Z',
                        'completed': True,
                        'user': 0,
                    }]
                },
            ),
            '401': openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail':
                            'Authentication credentials were not provided.'
                    },
                },
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        responses={
            '204': openapi.Response(
                description='No content',
            ),
            '401': openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail':
                            'Authentication credentials were not provided.'
                    },
                },
                schema=TaskSerializer,
            ),
            '404': openapi.Response(
                description='Not found',
                examples={
                    'application/json': {
                        'detail': 'Not found.'
                    },
                },
                schema=TaskSerializer,
            ),
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': {
                        'id': 0,
                        'title': 'string',
                        'description': 'string',
                        'start_date': '2019-08-24T14:15:22Z',
                        'end_date': '2019-08-24T14:15:22Z',
                        'completed': True,
                        'user': 0,
                    }
                },
                schema=TaskSerializer,
            ),
            '400': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'title': [
                            'This field may not be blank.',
                        ],
                    },
                },
                schema=TaskSerializer,
            ),
            '401': openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail':
                            'Authentication credentials were not provided.'
                    },
                },
                schema=TaskSerializer,
            ),
            '404': openapi.Response(
                description='Not found',
                examples={
                    'application/json': {
                        'detail': 'Not found.'
                    },
                },
                schema=TaskSerializer,
            ),
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': {
                        'id': 0,
                        'title': 'string',
                        'description': 'string',
                        'start_date': '2019-08-24T14:15:22Z',
                        'end_date': '2019-08-24T14:15:22Z',
                        'completed': True,
                        'user': 0,
                    }
                },
                schema=TaskSerializer,
            ),
            '400': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'title': [
                            'This field may not be blank.',
                        ],
                    },
                },
                schema=TaskSerializer,
            ),
            '401': openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail':
                            'Authentication credentials were not provided.'
                    },
                },
                schema=TaskSerializer,
            ),
            '404': openapi.Response(
                description='Not found',
                examples={
                    'application/json': {
                        'detail': 'Not found.'
                    },
                },
                schema=TaskSerializer,
            ),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': {
                        'id': 0,
                        'title': 'string',
                        'description': 'string',
                        'start_date': '2019-08-24T14:15:22Z',
                        'end_date': '2019-08-24T14:15:22Z',
                        'completed': True,
                        'user': 0,
                    }
                },
                schema=TaskSerializer,
            ),
            '401': openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail':
                            'Authentication credentials were not provided.'
                    },
                },
                schema=TaskSerializer,
            ),
            '404': openapi.Response(
                description='Not found',
                examples={
                    'application/json': {
                        'detail': 'Not found.'
                    },
                },
                schema=TaskSerializer,
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            '201': openapi.Response(
                description='Created',
                examples={
                    'application/json': {
                        'id': 0,
                        'title': "string",
                        'description': 'string',
                        'start_date': "2019-08-24T14:15:22Z",
                        'end_date': "2019-08-24T14:15:22Z",
                        'user': 0
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
                        'refresh': ['This field may not be blank.'],
                    },
                },
                schema=serializers.TokenRefreshSerializer,
            ),
            '401': openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail': 'Token is invalid or expired',
                        'code': 'token_not_valid',
                    },
                },
                schema=serializers.TokenRefreshSerializer,
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedToSwaggerTokenVerifyView(views.TokenVerifyView):

    @swagger_auto_schema(
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': {},
                },
                schema=serializers.TokenVerifySerializer,
            ),
            '400': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'token': ['This field may not be blank.'],
                    },
                },
                schema=serializers.TokenVerifySerializer,
            ),
            '401': openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail': 'Token is invalid or expired',
                        'code': 'token_not_valid',
                    },
                },
                schema=serializers.TokenVerifySerializer,
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedToSwaggerTokenObtainPairView(views.TokenObtainPairView):

    @swagger_auto_schema(
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': {
                        'username': 'string',
                        'password': 'string',
                    },
                },
                schema=serializers.TokenObtainPairSerializer,
            ),
            '400': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'username': [
                            'This field may not be blank.',
                        ],
                        'password': [
                            'This field may not be blank.',
                        ],
                    },
                },
                schema=serializers.TokenObtainPairSerializer,
            ),
            '401': openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail': ('No active account found with the '
                                   'given credentials'),
                    },
                },
                schema=serializers.TokenObtainPairSerializer,
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
