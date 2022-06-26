import pytest
from django.urls import reverse
from rest_framework import status

from api.models import User, Task


class TestCreateTask:

    @pytest.mark.django_db
    def test_create_task_by_user(
            self,
            client,
            set_of_authenticated_accounts_data,
            convert_date_class_to_iso_format,
    ):
        url = reverse('task-list')
        data = {
            'title': 'string',
            'description': 'string',
            'start_date': '2019-08-24T14:15:22Z',
            'end_date': '2019-10-24T14:15:22Z',
        }
        auth_header = (
            'Bearer '
            f'{set_of_authenticated_accounts_data["authenticated_account1"]["access-token"]}'
        )

        response = client.post(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.count() == 1

        task = Task.objects.get(id=response.data['id'])
        assert task.title == response.data['title']
        assert task.description == response.data['description']

        start_date = convert_date_class_to_iso_format(task.start_date)
        assert start_date == response.data['start_date']

        end_date = convert_date_class_to_iso_format(task.end_date)
        assert end_date == response.data['end_date']

        assert task.user.id == response.data['user']

    @pytest.mark.django_db
    def test_send_invalid_body(
            self,
            client,
            set_of_authenticated_accounts_data,
    ):
        url = reverse('task-list')
        data = {
            'description': 'string',
            'start_date': 'string',
            'end_date': '2019-10-24T14:15:22Z',
        }
        auth_header = (
            'Bearer '
            f'{set_of_authenticated_accounts_data["authenticated_account1"]["access-token"]}'
        )

        response = client.post(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'][0].code == 'required'
        assert response.data['start_date'][0].code == 'invalid'

        assert Task.objects.count() == 0

    @pytest.mark.django_db
    def test_create_task_with_same_enddate_startdate(
            self,
            client,
            set_of_authenticated_accounts_data,
            convert_date_class_to_iso_format,
    ):
        url = reverse('task-list')
        data = {
            'title': 'string',
            'description': 'string',
            'start_date': '2019-08-24T14:15:22Z',
            'end_date': '2019-08-24T14:15:22Z',
        }
        auth_header = (
            'Bearer '
            f'{set_of_authenticated_accounts_data["authenticated_account1"]["access-token"]}'
        )

        response = client.post(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['date'][0].code == 'invalid'

        assert Task.objects.count() == 0

    @pytest.mark.django_db
    def test_create_task_by_unauthorized_user(self, client):
        url = reverse('task-list')
        data = {
            'title': 'string',
            'description': 'string',
            'start_date': '2019-08-24T14:15:22Z',
            'end_date': '2019-10-24T14:15:22Z',
        }

        response = client.post(
            url,
            data=data,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'].code == 'not_authenticated'

        assert Task.objects.count() == 0


class TestRetrieveTask:

    @pytest.mark.django_db
    def test_retrieve_task_by_author(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
            convert_date_class_to_iso_format,
    ):
        url = reverse('task-detail', args=[set_of_tasks_data['task1'].id])
        auth_header = (
            'Bearer '
            f'{set_of_authenticated_accounts_data["authenticated_account1"]["access-token"]}'
        )

        response = client.get(
            url,
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_200_OK

        task = set_of_tasks_data['task1']
        assert task.title == response.data['title']
        assert task.description == response.data['description']
        assert task.start_date == response.data['start_date']
        assert task.end_date == response.data['end_date']
        assert task.user.id == response.data['user']

        assert task.user == User.objects.get(
            username=set_of_authenticated_accounts_data['authenticated_account1']['username']
        )

    @pytest.mark.django_db
    def test_retrieve_invalid_task_id(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
    ):
        url = reverse('task-detail', args=[Task.objects.count() + 1])
        auth_header = (
            'Bearer '
            f'{set_of_authenticated_accounts_data["authenticated_account1"]["access-token"]}'
        )

        response = client.get(
            url,
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'].code == 'not_found'

    @pytest.mark.django_db
    def test_retrieve_task_by_another_user(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
    ):
        url = reverse('task-detail', args=[set_of_tasks_data['task1'].id])
        auth_header = (
            'Bearer '
            f'{set_of_authenticated_accounts_data["authenticated_account2"]["access-token"]}'
        )

        response = client.get(
            url,
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'].code == 'not_found'

    @pytest.mark.django_db
    def test_retrieve_task_by_unauthorized_user(
            self,
            client,
            set_of_tasks_data,
    ):
        url = reverse('task-detail', args=[set_of_tasks_data['task1'].id])

        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'].code == 'not_authenticated'


class TestDeleteTask:

    @pytest.mark.django_db
    def test_delete_task_by_author(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
    ):
        id = set_of_tasks_data['task1'].id
        url = reverse('task-detail', args=[id])
        auth_header = (
            'Bearer '
            f'{set_of_authenticated_accounts_data["authenticated_account1"]["access-token"]}'
        )

        response = client.delete(
            url,
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Task.objects.filter(id=id).count() == 0

    @pytest.mark.django_db
    def test_delete_invalid_task_id(
            self,
            client,
            set_of_authenticated_accounts_data,
    ):
        id = Task.objects.count() + 1
        url = reverse('task-detail', args=[id])
        auth_header = (
            'Bearer '
            f'{set_of_authenticated_accounts_data["authenticated_account1"]["access-token"]}'
        )

        response = client.delete(
            url,
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'].code == 'not_found'

    @pytest.mark.django_db
    def test_delete_task_by_another_user(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
    ):
        id = set_of_tasks_data['task1'].id
        url = reverse('task-detail', args=[id])
        auth_header = (
            'Bearer '
            f'{set_of_authenticated_accounts_data["authenticated_account2"]["access-token"]}'
        )

        response = client.delete(
            url,
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'].code == 'not_found'
        assert Task.objects.filter(id=id).count() == 1

    @pytest.mark.django_db
    def test_delete_task_by_unauthorized_user(
            self,
            client,
            set_of_tasks_data,
    ):
        id = set_of_tasks_data['task1'].id
        url = reverse('task-detail', args=[id])

        response = client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'].code == 'not_authenticated'
        assert Task.objects.filter(id=id).count() == 1


class TestListTask:

    @pytest.mark.django_db
    def test_list_task_by_author(
            self,
            client,
            set_of_authenticated_accounts_data,
            convert_date_class_to_iso_format,
    ):
        url = reverse('task-list')
        auth_header = (
            'Bearer '
            f'{set_of_authenticated_accounts_data["authenticated_account1"]["access-token"]}'
        )

        response = client.get(
            url,
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_200_OK

        for resp in response.data:
            task = Task.objects.filter(id=resp['id'])
            
            assert convert_date_class_to_iso_format(task[0].start_date) == resp['start_date']
            assert convert_date_class_to_iso_format(task[0].end_date) == resp['end_date']
            assert task[0].description == resp['description']
            assert task[0].title == resp['title']
            assert task[0].user.id == resp['user']
            
    @pytest.mark.django_db
    def test_list_task_by_unauthorized_user(
            self,
            client,
    ):
        url = reverse('task-list')

        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'].code == 'not_authenticated'
    
    @pytest.mark.django_db
    def test_list_task_with_2_users(
            self,
            client,
            set_of_authenticated_accounts_data,
            convert_date_class_to_iso_format,
    ):
        url = reverse('task-list')
        auth_header_for_author = (
            'Bearer '
            f'{set_of_authenticated_accounts_data["authenticated_account1"]["access-token"]}'
        )
        response = client.get(
            url,
            HTTP_AUTHORIZATION=auth_header_for_author,
        )

        auth_header_for_second_user = (
            'Bearer '
            f'{set_of_authenticated_accounts_data["authenticated_account2"]["access-token"]}'
        )
        second_response = client.get(
            url,
            HTTP_AUTHORIZATION=auth_header_for_second_user,
        )

        assert response.status_code == status.HTTP_200_OK

        for resp in response.data:
            task = Task.objects.filter(id=resp['id'])
            
            assert convert_date_class_to_iso_format(task[0].start_date) == resp['start_date']
            assert convert_date_class_to_iso_format(task[0].end_date) == resp['end_date']
            assert task[0].description == resp['description']
            assert task[0].title == resp['title']
            assert task[0].user.id == resp['user']
            assert task[0].user.id != second_response['user']
