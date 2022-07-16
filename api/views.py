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

example_task = {
    'id': 1,
    'title': 'string',
    'description': 'string',
    'start_date': '2022-06-05T10:15:00Z',
    'end_date': '2022-06-05T10:20:00Z',
    'completed': True,
    'user': 1,
}

open_api_400_required_title = openapi.Response(
    description='Bad Request',
    examples={
        'application/json': {
            'title': 'This field is required.',
        },
    },
    schema=TaskSerializer, # Тут нужно поменять
)

open_api_400_required_start_date = openapi.Response(
    description='Bad Request',
    examples={
        'application/json': {
            'start_date': 'This field is required.',
        },
    },
    schema=TaskSerializer, # Тут нужно поменять
)

open_api_400_required_end_date = openapi.Response(
    description='Bad Request',
    examples={
        'application/json': {
            'end_date': 'This field is required.',
        },
    },
    schema=TaskSerializer, # Тут нужно поменять
)

open_api_400_blank_title = openapi.Response(
    description='Bad Request',
    examples={
        'application/json': {
            'title': 'This field may not be blank.',
        },
    },
    schema=TaskSerializer, # Тут нужно поменять
)

open_api_400_blank_start_date = openapi.Response(
    description='Bad Request',
    examples={
        'application/json': {
            'start_date': 'Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].',
        },
    },
    schema=TaskSerializer, # Тут нужно поменять
)

open_api_400_blank_end_date = openapi.Response(
    description='Bad Request',
    examples={
        'application/json': {
            'end_date': 'Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].',
        },
    },
    schema=TaskSerializer, # Тут нужно поменять
)

open_api_400_blank_username = openapi.Response(
    description='Bad request',
    examples={
        'application/json': {
            'username': 'This field may not be blank.',
        },
    },
    schema=serializers.TokenObtainPairSerializer,  # Тут нужно поменять
)

open_api_400_blank_email = openapi.Response(
    description='Bad request',
    examples={
        'application/json': {
            'username': 'This field may not be blank.',
        },
    },
    schema=serializers.TokenObtainPairSerializer,  # Тут нужно поменять
)

open_api_400_blank_password = openapi.Response(
    description='Bad request',
    examples={
        'application/json': {
            'password': 'This field may not be blank.',
        },
    },
    schema=serializers.TokenObtainPairSerializer,  # Тут нужно поменять
)

open_api_401_token = openapi.Response(
    description='Unautorized',
    examples={
        'application/json': {
            'detail': 'Token is invalid or expired',
            'code': 'token_not_valid'
        },
    },
    schema=TaskSerializer, # Тут нужно поменять
)

open_api_401_token_type = openapi.Response(
    description='Unautorized',
    examples={
        'application/json': {
            'detail': 'Token has wrong type',
            'code': 'token_not_valid'
        },
    },
    schema=TaskSerializer, # Тут нужно поменять
)

open_api_401_tasks_token = openapi.Response(
    description='Unautorized',
    examples={
        'application/json': {
           'detail': "Given token not valid for any token type",
            'code': "token_not_valid",
            'messages': [
                {
                    'token_class': 'AccessToken',
                    'token_type': 'access',
                    'message': 'Token is invalid or expired'
                }
            ]
        },
    },
    schema=TaskSerializer, # Тут нужно поменять
)

open_api_404 = openapi.Response(
    description='Not found',
    examples={
        'application/json': {
            'detail': 'Not found.'
        },
    },
    schema=TaskSerializer, # Тут нужно поменять
)

open_api_415 = openapi.Response(
    description='Unsupported Media Type',
    examples={
        'application/json': {
            'detail': 'Unsupported media type "text/plain" in request.'
        },
    },
    schema=TaskSerializer, # Тут нужно поменять
)

class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    # POST /register/
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
            '400': open_api_400_blank_username,
            '400 (blank email)': open_api_400_blank_email,
            '400 (blank password)': open_api_400_blank_password,
            '400 (exist username)': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'username': 'A user with that username already exists.',
                    },
                },
                schema=RegisterSerializer,
            ),
            '400 (exist email)': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'email': 'A user with this email already exist',
                    },
                },
                schema=RegisterSerializer,
            ),
            '400 (password 8 char)': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'password': 'This password is too short. It must contain at least 8 characters.',
                    },
                },
                schema=RegisterSerializer,
            ),
            '400 (password num)': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'password': 'This password is entirely numeric.',
                    },
                },
                schema=RegisterSerializer,
            ),
            '400 (password up)': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'password': 'This password must contain at least 1 upper case letter.',
                    },
                },
                schema=RegisterSerializer,
            ),
            '400 (password special)': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'password': 'This password must contain at least 1 special character.',
                    },
                },
                schema=RegisterSerializer,
            ),
            '415': open_api_415,
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

    # GET /tasks/statuses/
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
            '401': open_api_401_tasks_token,
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

    # GET /tasks/
    @swagger_auto_schema(
        manual_parameters=[year_param, month_param, day_param],
        security=[{'Bearer': []}],
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': [
                        example_task,
                    ]
                },
                schema=TaskSerializer,
            ),
            '401': open_api_401_tasks_token
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

    # DELETE /tasks/{id}/
    @swagger_auto_schema(
        security=[{'Bearer': []}],
        responses={
            '204': openapi.Response(
                description='No content',
            ),
            '401': open_api_401_tasks_token,
            '404': open_api_404,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # PUT /tasks/{id}/
    @swagger_auto_schema(
        security=[{'Bearer': []}],
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': example_task,
                },
                schema=TaskSerializer,
            ),
            '400': open_api_400_required_title,
            '400 (required start_date)': open_api_400_required_start_date,
            '400 (required end_date)': open_api_400_required_end_date,
            '400 (blank title)': open_api_400_blank_title,
            '400 (blank start_date)': open_api_400_blank_start_date,
            '400 (blank end_date)': open_api_400_blank_end_date,
            '401': open_api_401_tasks_token,
            '404': open_api_404,
            '415': open_api_415,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # PATCH /tasks/{id}/
    @swagger_auto_schema(
        security=[{'Bearer': []}],
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': example_task,
                },
                schema=TaskSerializer,
            ),
            '401': open_api_401_tasks_token,
            '404': open_api_404,
            '415': open_api_415,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # GET /tasks/{id}/
    @swagger_auto_schema(
        security=[{'Bearer': []}],
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': example_task,
                },
                schema=TaskSerializer,
            ),
            '401': open_api_401_tasks_token,
            '404': open_api_404,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # POST /tasks/
    @swagger_auto_schema(
        security=[{'Bearer': []}],
        responses={
            '201': openapi.Response(
                description='Created',
                examples={
                    'application/json': example_task,
                },
                schema=TaskSerializer,
            ),
            '400': open_api_400_required_title,
            '400 (required start_date)': open_api_400_required_start_date,
            '400 (required end_date)': open_api_400_required_end_date,
            '400 (blank title)': open_api_400_blank_title,
            '400 (blank start_date)': open_api_400_blank_start_date,
            '400 (blank end_date)': open_api_400_blank_end_date,
            '401': open_api_401_tasks_token,
            '415': open_api_415,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class DecoratedToSwaggerTokenRefreshView(views.TokenRefreshView):

    # POST /refresh-token/
    @swagger_auto_schema(
        security=[{'Basic': []}],
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': {
                        'access': '36symbols.150symbols.43symbols',
                    },
                },
                schema=serializers.TokenRefreshSerializer, # Тут нужно поменять
            ),
            '400': openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'refresh': 'This field may not be blank.'
                    },
                },
                schema=serializers.TokenRefreshSerializer,  # Тут нужно поменять
            ),
            '401': open_api_401_token,
            '401 (type)': open_api_401_token_type,
            '415': open_api_415,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedToSwaggerTokenVerifyView(views.TokenVerifyView):

    # POST /verify-token/
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
                        'token': 'This field may not be blank.',
                    },
                },
                schema=serializers.TokenVerifySerializer,
            ),
            '401': open_api_401_token,
            '415': open_api_415,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedToSwaggerTokenObtainPairView(views.TokenObtainPairView):

    # POST /login/
    @swagger_auto_schema(
        security=[{'Basic': []}],
        responses={
            '200': openapi.Response(
                description='Ok',
                examples={
                    'application/json': {
                        'refresh': '36symbols.150symbols.43symbols',
                        'access': '36symbols.150symbols.43symbols',
                    },
                },
                schema=serializers.TokenObtainPairSerializer,
            ),
            '400': open_api_400_blank_username,
            '400 (blank password)': open_api_400_blank_password,
            '401': openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail': 'No active account found with the given credentials'
                    },
                },
                schema=serializers.TokenObtainPairSerializer,
            ),
            '415': open_api_415,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
