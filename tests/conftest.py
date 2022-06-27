import datetime

import pytest
from django.urls import reverse

from api.models import User, Task
from api.serializers import RegisterSerializer


@pytest.fixture
def set_of_users_data():
    """Create set of users."""
    user1 = User.objects.create(
        username='testuser',
        email='testuser@mail.ru',
        password='1234',
    )
    user2 = User.objects.create(
        username='usertest',
        email='usertest@mail.ru',
        password='1234',
    )

    return {'user1': user1, 'user2': user2}


@pytest.fixture
def set_of_accounts_data():
    """Create set of accounts."""
    account1 = {
        'username': 'testacc',
        'email': 'testacc@mail.ru',
        'password': '1234',
    }

    serializer = RegisterSerializer(data=account1)
    serializer.is_valid()
    serializer.save()

    account2 = {
        'username': 'useracc',
        'email': 'useracc@mail.ru',
        'password': '1234',
    }
    serializer = RegisterSerializer(data=account2)
    serializer.is_valid()
    serializer.save()

    return {'account1': account1, 'account2': account2}


@pytest.fixture
def set_of_authenticated_accounts_data(client, set_of_accounts_data):
    """Create set of authenticated accounts."""
    url = reverse('token_obtain_pair')
    authenticated_account1 = {
        'username': set_of_accounts_data['account1']['username'],
        'password': set_of_accounts_data['account1']['password']
    }

    response = client.post(url, data=authenticated_account1)

    authenticated_account1['access-token'] = response.data['access']
    authenticated_account1['refresh-token'] = response.data['refresh']

    authenticated_account2 = {
        'username': set_of_accounts_data['account2']['username'],
        'password': set_of_accounts_data['account2']['password']
    }

    response = client.post(url, data=authenticated_account2)

    authenticated_account2['access-token'] = response.data['access']
    authenticated_account2['refresh-token'] = response.data['refresh']
    return {
        'authenticated_account1': authenticated_account1,
        'authenticated_account2': authenticated_account2,
    }


@pytest.fixture
def set_of_tasks_data(client, set_of_accounts_data):
    """Create set of authenticated accounts."""
    username = set_of_accounts_data['account1']['username']
    account1 = User.objects.get(username=username)

    task1 = Task.objects.create(
        title='task1',
        description='string1',
        start_date='2019-08-24T14:15:22Z',
        end_date='2019-10-24T14:15:22Z',
        user=account1
    )
    task2 = Task.objects.create(
        title='task2',
        description='string2',
        start_date='2019-08-24T14:15:22Z',
        end_date='2019-10-24T14:15:22Z',
        user=account1
    )

    username = set_of_accounts_data['account2']['username']
    account2 = User.objects.get(username=username)

    task3 = Task.objects.create(
        title='task3',
        description='string3',
        start_date='2019-08-24T14:15:22Z',
        end_date='2019-10-24T14:15:22Z',
        user=account2
    )
    task4 = Task.objects.create(
        title='task4',
        description='string4',
        start_date='2019-08-24T14:15:22Z',
        end_date='2019-10-24T14:15:22Z',
        user=account2
    )

    return {
        'task1': task1, 'task2': task2, 'task3': task3, 'task4': task4,
    }


@pytest.fixture
def convert_date_class_to_iso_format():
    def converter(date: datetime.datetime) -> str:
        return date.strftime("%Y-%m-%dT%H:%M:%SZ",)

    return converter
