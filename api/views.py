from datetime import datetime

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import views, serializers
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import User, Task
from .serializers import (
    RegisterSerializer,
    TaskSerializer,
    TaskStatusesSerializer,
)


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        security=[{'Basic': []}],
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

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'statuses':
            return TaskStatusesSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        security=[{'Bearer': []}],
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': [
                        {
                            'date': '2019-08-24',
                            'completed': True,
                            'not_completed': True,
                        }
                    ]
                },
                schema=TaskStatusesSerializer,
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
    @action(detail=False, methods=['GET'])
    def statuses(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = {}

        for task in queryset:
            date = task.start_date
            key = datetime(year=date.year, month=date.month, day=date.day)

            if key not in data:
                data[key] = {
                    'completed': False,
                    'not_completed': False,
                }

            if task.completed:
                data[key]['completed'] = True
            else:
                data[key]['not_completed'] = True

        statuses = []
        for date, status in data.items():
            statuses.append(
                {
                    'date': date,
                    'completed': status['completed'],
                    'not_completed': status['not_completed'],
                }
            )
        statuses.sort(key=lambda x: x['date'])

        serializer = self.get_serializer_class()
        serializer = serializer(data=statuses, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    year_param = openapi.Parameter(
        'year',
        openapi.IN_QUERY,
        description='year in start_date field',
        type=openapi.TYPE_NUMBER
    )
    month_param = openapi.Parameter(
        'month',
        openapi.IN_QUERY,
        description='month in start_date field',
        type=openapi.TYPE_NUMBER
    )
    day_param = openapi.Parameter(
        'day',
        openapi.IN_QUERY,
        description='day in start_date field',
        type=openapi.TYPE_NUMBER
    )

    @swagger_auto_schema(
        manual_parameters=[year_param, month_param, day_param],
        security=[{'Bearer': []}],
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': [
                        {
                            'id': 0,
                            'title': 'string',
                            'description': 'string',
                            'start_date': '2019-08-24T14:15:22Z',
                            'end_date': '2019-08-24T14:15:22Z',
                            'completed': True,
                            'user': 0,
                        }
                    ]
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
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if 'year' in request.query_params:
            year = request.query_params.get('year')
            queryset = queryset.filter(start_date__year=year)

        if 'month' in request.query_params:
            month = request.query_params.get('month')
            queryset = queryset.filter(start_date__month=month)

        if 'day' in request.query_params:
            day = request.query_params.get('day')
            queryset = queryset.filter(start_date__day=day)

        queryset = queryset.order_by('start_date')
        serializer = self.get_serializer_class()
        serializer = serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        security=[{'Bearer': []}],
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
            ),
            '404': openapi.Response(
                description='Not found',
                examples={
                    'application/json': {
                        'detail': 'Not found.'
                    },
                },
            ),
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        security=[{'Bearer': []}],
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
            ),
            '404': openapi.Response(
                description='Not found',
                examples={
                    'application/json': {
                        'detail': 'Not found.'
                    },
                },
            ),
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        security=[{'Bearer': []}],
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
            ),
            '404': openapi.Response(
                description='Not found',
                examples={
                    'application/json': {
                        'detail': 'Not found.'
                    },
                },
            ),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        security=[{'Bearer': []}],
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
            ),
            '404': openapi.Response(
                description='Not found',
                examples={
                    'application/json': {
                        'detail': 'Not found.'
                    },
                },
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        security=[{'Bearer': []}],
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
                        'detail':
                            "Authentication credentials were not provided."
                    },
                },
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class DecoratedToSwaggerTokenRefreshView(views.TokenRefreshView):

    @swagger_auto_schema(
        security=[{'Basic': []}],
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
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedToSwaggerTokenVerifyView(views.TokenVerifyView):

    @swagger_auto_schema(
        security=[{'Basic': []}],
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
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedToSwaggerTokenObtainPairView(views.TokenObtainPairView):

    @swagger_auto_schema(
        security=[{'Basic': []}],
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
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
