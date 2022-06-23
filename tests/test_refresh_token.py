import pytest

from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_correct_refresh_token(client, set_of_accounts_data):
    url = reverse('token_obtain_pair')
    data = {
        'username': set_of_accounts_data['account1']['username'],
        'password': set_of_accounts_data['account1']['password'],
    }
    response = client.post(url, data=data)

    url = reverse('token_refresh')
    data = {
        'refresh': response.data['refresh'],
    }
    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['access'] is not None


@pytest.mark.django_db
def test_blank_refresh_token(client):
    url = reverse('token_refresh')
    data = {
        'refresh': '',
    }
    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_invalid_refresh_token(client):
    url = reverse('token_refresh')
    data = {
        'refresh': 'invalid token',
    }
    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
