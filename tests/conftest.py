import pytest

from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.fixture
def set_of_users_data():
    """Create set of users"""
    user1 = User.objects.create(username='testuser', email='testuser@mail.ru', password='1234')
    user2 = User.objects.create(username='usertest', email='usertest@mail.ru', password='1234')

    return {'user1': user1, 'user2': user2}
