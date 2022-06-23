import pytest

from api.models import User
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
