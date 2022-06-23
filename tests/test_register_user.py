import pytest

from django.urls import reverse

from api.models import User


@pytest.mark.django_db
def test_new_user_register(client, django_user_model):
    utl = reverse('register-list')
    data = {
        'username': 'test',
        'email': 'test@mail.ru',
        'password': '1234',
    }
    response = client.post(utl, data=data)

    assert response.status_code == 201
    assert response.data['username'] == data['username']
    assert response.data['email'] == data['email']
    assert response.data.get('password') is None

    assert User.objects.count() == 1


@pytest.mark.django_db
def test_register_use_with_same_username(client, django_user_model, set_of_users_data):
    utl = reverse('register-list')
    data = {
        'username': set_of_users_data['user1'].username,
        'email': 'test@mail.ru',
        'password': '1234',
    }
    response = client.post(utl, data=data)

    assert response.status_code == 400
    assert 'username' in response.data
    assert User.objects.count() == len(list(set_of_users_data.keys()))


@pytest.mark.django_db
def test_register_use_with_same_email(client, django_user_model, set_of_users_data):
    utl = reverse('register-list')
    data = {
        'username': 'test',
        'email': set_of_users_data['user2'].email,
        'password': '1234',
    }
    response = client.post(utl, data=data)

    assert response.status_code == 400
    assert 'email' in response.data
    assert User.objects.count() == len(list(set_of_users_data.keys()))
