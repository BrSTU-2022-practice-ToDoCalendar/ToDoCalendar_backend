import pytest

from django.urls import reverse
from rest_framework import status

from api.models import User


@pytest.mark.django_db
def test_new_user_register(client):
    url = reverse('register-list')
    data = {
        'username': 'test',
        'email': 'test@mail.ru',
        'password': '123qeqweQ_4',
    }
    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == data['username']
    assert response.data['email'] == data['email']
    assert response.data.get('password') is None

    assert User.objects.get(username=data['username']).email == data['email']
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_register_user_with_same_username(client, set_of_users_data):
    url = reverse('register-list')
    data = {
        'username': set_of_users_data['user1'].username,
        'email': 'test@mail.ru',
        'password': '1234',
    }
    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data

    assert User.objects.count() == len(list(set_of_users_data.keys()))


@pytest.mark.django_db
def test_register_user_with_same_email(client, set_of_users_data):
    url = reverse('register-list')
    data = {
        'username': 'test',
        'email': set_of_users_data['user2'].email,
        'password': '1234',
    }
    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data

    assert User.objects.count() == len(list(set_of_users_data.keys()))


@pytest.mark.django_db
def test_new_user_with_invalid_email(client):
    url = reverse('register-list')
    data = {
        'username': 'test',
        'email': 'invalid_email',
        'password': '1234',
    }
    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data

    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_user_with_same_email_in_upper_case(
        client, set_of_users_data
):
    url = reverse('register-list')
    data = {
        'username': 'test',
        'email': set_of_users_data['user2'].email.upper(),
        'password': '1234',
    }
    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data

    assert User.objects.count() == len(list(set_of_users_data.keys()))
