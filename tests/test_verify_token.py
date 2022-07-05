import pytest

from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_verify_correct_token(client, set_of_accounts_data):
    url = reverse('token_obtain_pair')
    data = {
        'username': set_of_accounts_data['account1']['username'],
        'password': set_of_accounts_data['account1']['password'],
    }
    response = client.post(url, data=data)

    url = reverse('token_verify')
    data = {
        'token': response.data['access'],
    }

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert not response.data


@pytest.mark.django_db
def test_verify_incorrect_token(client):
    url = reverse('token_verify')
    data = {
        'token': 'invalid token',
    }
    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['code'] == 'token_not_valid'


@pytest.mark.django_db
def test_verify_blank_token(client):
    url = reverse('token_verify')
    data = {
        'token': '',
    }
    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['token'] is not None
