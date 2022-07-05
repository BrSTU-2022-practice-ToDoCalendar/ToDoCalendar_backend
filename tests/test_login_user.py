import pytest

from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_correct_user_login(client, set_of_accounts_data):
    url = reverse('token_obtain_pair')
    data = {
        'username': set_of_accounts_data['account1']['username'],
        'password': set_of_accounts_data['account1']['password'],
    }
    response = client.post(url, data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['access'] is not None
    assert response.data['refresh'] is not None


@pytest.mark.django_db
def test_invalid_user_login(client):
    url = reverse('token_obtain_pair')
    data = {
        'username': '2testacc2',
        'password': '1234',

    }
    response = client.post(url, data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'].code == 'no_active_account'


@pytest.mark.django_db
def test_blank_user_login(client):
    url = reverse('token_obtain_pair')
    data = {
        'username': ' ',
        'password': ' ',

    }
    response = client.post(url, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
