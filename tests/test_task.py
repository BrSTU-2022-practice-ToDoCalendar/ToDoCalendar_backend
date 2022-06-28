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

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (
            'Bearer '
            f'{acc["access-token"]}'
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

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (
            'Bearer '
            f'{acc["access-token"]}'
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

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (
            'Bearer '
            f'{acc["access-token"]}'
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

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (
            'Bearer '
            f'{acc["access-token"]}'
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
            username=acc['username']
        )

    @pytest.mark.django_db
    def test_retrieve_invalid_task_id(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
    ):
        url = reverse('task-detail', args=[Task.objects.count() + 1])

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (
            'Bearer '
            f'{acc["access-token"]}'
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

        acc = set_of_authenticated_accounts_data['authenticated_account2']
        auth_header = (
            'Bearer '
            f'{acc["access-token"]}'
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

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (
            'Bearer '
            f'{acc["access-token"]}'
        )

        response = client.delete(
            url,
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(id=id).exists()

    @pytest.mark.django_db
    def test_delete_invalid_task_id(
            self,
            client,
            set_of_authenticated_accounts_data,
    ):
        id = Task.objects.count() + 1
        url = reverse('task-detail', args=[id])

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (
            'Bearer '
            f'{acc["access-token"]}'
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

        acc = set_of_authenticated_accounts_data['authenticated_account2']
        auth_header = (
            'Bearer '
            f'{acc["access-token"]}'
        )

        response = client.delete(
            url,
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'].code == 'not_found'
        assert Task.objects.get(id=id)

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
            set_of_tasks_data,
            set_of_accounts_data,
    ):
        url = reverse('task-list')
        
        account = set_of_authenticated_accounts_data["authenticated_account1"]
        auth_header = (
            'Bearer '
            f'{account["access-token"]}'
        )

        response = client.get(
            url,
            HTTP_AUTHORIZATION=auth_header,
        )
        
        tasks = Task.objects.filter(
            user__username = account['username']
        )

        assert response.status_code == status.HTTP_200_OK
        assert tasks.count() == len(response.data)

        for resp in response.data:
            task = tasks.get(id = resp['id'])

            assert convert_date_class_to_iso_format(task.start_date) == resp['start_date']
            assert convert_date_class_to_iso_format(task.end_date) == resp['end_date']
            assert task.description == resp['description']
            assert task.title == resp['title']
            assert task.user.id == resp['user']
            assert account['username'] == task.user.username
            
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
            set_of_tasks_data,
            set_of_accounts_data,
    ):
        url = reverse('task-list')
        account = set_of_authenticated_accounts_data["authenticated_account1"]
        auth_header_for_author = (
            'Bearer '
            f'{account["access-token"]}'
        )
        response = client.get(
            url,
            HTTP_AUTHORIZATION=auth_header_for_author,
        )

        second_account = set_of_authenticated_accounts_data["authenticated_account2"]
        second_user_tasks = Task.objects.filter(
            user__username=second_account['username']
        )

        assert response.status_code == status.HTTP_200_OK
        
        for resp in response.data:
            assert not second_user_tasks.filter(id = resp['id']).exists()
        assert Task.objects.get(id=id)


class TestUpdateTask:

    @pytest.mark.django_db
    def test_correct_patch_all_fields_by_author(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
            convert_date_class_to_iso_format,
    ):
        id = set_of_tasks_data['task1'].id
        url = reverse('task-detail', args=[id])

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (f'Bearer {acc["access-token"]}')
        data = {
            'title': 'new_title',
            'description': 'new_description',
            'start_date': '2000-08-24T14:15:22Z',
            'end_date': '2000-10-24T14:15:22Z',
        }

        response = client.patch(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_200_OK

        task = Task.objects.get(id=id)

        assert task.title == data['title']
        assert task.description == data['description']

        start_date = convert_date_class_to_iso_format(task.start_date)
        assert start_date == data['start_date']

        end_date = convert_date_class_to_iso_format(task.end_date)
        assert end_date == data['end_date']

        assert task.user.username == acc['username']

    @pytest.mark.django_db
    def test_correct_patch_all_fields_by_another_user(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
            convert_date_class_to_iso_format,
    ):
        id = set_of_tasks_data['task3'].id
        url = reverse('task-detail', args=[id])

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (f'Bearer {acc["access-token"]}')
        data = {
            'title': 'new_title',
            'description': 'new_description',
            'start_date': '2000-08-24T14:15:22Z',
            'end_date': '2000-10-24T14:15:22Z',
        }

        response = client.patch(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'].code == 'not_found'

        task = Task.objects.get(id=id)

        assert task.title != data['title']
        assert task.description != data['description']

        start_date = convert_date_class_to_iso_format(task.start_date)
        assert start_date != data['start_date']

        end_date = convert_date_class_to_iso_format(task.end_date)
        assert end_date != data['end_date']

    @pytest.mark.django_db
    def test_correct_patch_all_fields_by_unauthorized_user(
            self,
            client,
            set_of_tasks_data,
            convert_date_class_to_iso_format,
    ):
        id = set_of_tasks_data['task1'].id
        url = reverse('task-detail', args=[id])

        data = {
            'title': 'new_title',
            'description': 'new_description',
            'start_date': '2000-08-24T14:15:22Z',
            'end_date': '2000-10-24T14:15:22Z',
        }

        response = client.patch(
            url,
            data=data,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'].code == 'not_authenticated'

        task = Task.objects.get(id=id)

        assert task.title != data['title']
        assert task.description != data['description']

        start_date = convert_date_class_to_iso_format(task.start_date)
        assert start_date != data['start_date']

        end_date = convert_date_class_to_iso_format(task.end_date)
        assert end_date != data['end_date']

    @pytest.mark.django_db
    def test_invalid_patch_all_fields_by_authorized_user(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
    ):
        id = Task.objects.count() + 1
        url = reverse('task-detail', args=[id])

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (f'Bearer {acc["access-token"]}')
        data = {
            'title': 'new_title',
            'description': 'new_description',
            'start_date': '2000-08-24T14:15:22Z',
            'end_date': '2000-10-24T14:15:22Z',
        }

        response = client.patch(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'].code == 'not_found'

    @pytest.mark.django_db
    def test_invalid_patch_all_fields_with_same_startdate_enddate_by_author(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
            convert_date_class_to_iso_format,
    ):
        id = set_of_tasks_data['task1'].id
        url = reverse('task-detail', args=[id])

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (f'Bearer {acc["access-token"]}')
        data = {
            'title': 'new_title',
            'description': 'new_description',
            'start_date': '2000-08-24T14:15:22Z',
            'end_date': '2000-08-24T14:15:22Z',
        }

        response = client.patch(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['date'][0].code == 'invalid'

        task = Task.objects.get(id=id)

        assert task.title != data['title']
        assert task.description != data['description']

        start_date = convert_date_class_to_iso_format(task.start_date)
        assert start_date != data['start_date']

        end_date = convert_date_class_to_iso_format(task.end_date)
        assert end_date != data['end_date']

        assert task.user.username == acc['username']

    @pytest.mark.django_db
    def test_correct_patch_title_field_by_author(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
            convert_date_class_to_iso_format,
    ):
        id = set_of_tasks_data['task1'].id
        url = reverse('task-detail', args=[id])

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (f'Bearer {acc["access-token"]}')
        data = {
            'title': 'new_title',
        }

        response = client.patch(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_200_OK

        task = Task.objects.get(id=id)

        assert task.title == data['title']
        assert task.description == set_of_tasks_data['task1'].description

        start_date = convert_date_class_to_iso_format(task.start_date)
        assert start_date == set_of_tasks_data['task1'].start_date

        end_date = convert_date_class_to_iso_format(task.end_date)
        assert end_date == set_of_tasks_data['task1'].end_date
        assert task.user.username == acc['username']

    @pytest.mark.django_db
    def test_correct_patch_description_field_by_author(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
            convert_date_class_to_iso_format,
    ):
        id = set_of_tasks_data['task1'].id
        url = reverse('task-detail', args=[id])

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (f'Bearer {acc["access-token"]}')
        data = {
            'description': 'new_description',
        }

        response = client.patch(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_200_OK

        task = Task.objects.get(id=id)

        assert task.title == set_of_tasks_data['task1'].title

        assert task.description == data['description']

        start_date = convert_date_class_to_iso_format(task.start_date)
        assert start_date == set_of_tasks_data['task1'].start_date

        end_date = convert_date_class_to_iso_format(task.end_date)
        assert end_date == set_of_tasks_data['task1'].end_date
        assert task.user.username == acc['username']

    @pytest.mark.django_db
    def test_correct_patch_startdate_field_by_author(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
            convert_date_class_to_iso_format,
    ):
        id = set_of_tasks_data['task1'].id
        url = reverse('task-detail', args=[id])

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (f'Bearer {acc["access-token"]}')
        data = {
            'start_date': '2000-12-01T00:00:00Z',
        }

        response = client.patch(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_200_OK

        task = Task.objects.get(id=id)

        assert task.title == set_of_tasks_data['task1'].title
        assert task.description == set_of_tasks_data['task1'].description

        start_date = convert_date_class_to_iso_format(task.start_date)
        assert start_date == data['start_date']

        end_date = convert_date_class_to_iso_format(task.end_date)
        assert end_date == set_of_tasks_data['task1'].end_date
        assert task.user.username == acc['username']

    @pytest.mark.django_db
    def test_correct_patch_enddate_field_by_author(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
            convert_date_class_to_iso_format,
    ):
        id = set_of_tasks_data['task1'].id
        url = reverse('task-detail', args=[id])

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (f'Bearer {acc["access-token"]}')
        data = {
            'end_date': '2020-12-01T00:00:00Z',
        }

        response = client.patch(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_200_OK

        task = Task.objects.get(id=id)

        assert task.title == set_of_tasks_data['task1'].title
        assert task.description == set_of_tasks_data['task1'].description
        start_date = convert_date_class_to_iso_format(task.start_date)
        assert start_date == set_of_tasks_data['task1'].start_date

        end_date = convert_date_class_to_iso_format(task.end_date)
        assert end_date == data['end_date']

        assert task.user.username == acc['username']

    @pytest.mark.django_db
    def test_invalid_patch_startdate_field_by_author(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
            convert_date_class_to_iso_format,
    ):
        id = set_of_tasks_data['task1'].id
        url = reverse('task-detail', args=[id])

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (f'Bearer {acc["access-token"]}')
        data = {
            'start_date': '2020-12-01T00:00:00Z',
        }

        response = client.patch(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['date'][0].code == 'invalid'

        task = Task.objects.get(id=id)

        assert task.title == set_of_tasks_data['task1'].title
        assert task.description == set_of_tasks_data['task1'].description

        start_date = convert_date_class_to_iso_format(task.start_date)
        assert start_date != data['start_date']

        end_date = convert_date_class_to_iso_format(task.end_date)
        assert end_date == set_of_tasks_data['task1'].end_date
        assert task.user.username == acc['username']

    @pytest.mark.django_db
    def test_invalid_patch_enddate_field_by_author(
            self,
            client,
            set_of_authenticated_accounts_data,
            set_of_tasks_data,
            convert_date_class_to_iso_format,
    ):
        id = set_of_tasks_data['task1'].id
        url = reverse('task-detail', args=[id])

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = (f'Bearer {acc["access-token"]}')
        data = {
            'end_date': '2000-12-01T00:00:00Z',
        }

        response = client.patch(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['date'][0].code == 'invalid'

        task = Task.objects.get(id=id)

        assert task.title == set_of_tasks_data['task1'].title
        assert task.description == set_of_tasks_data['task1'].description
        start_date = convert_date_class_to_iso_format(task.start_date)
        assert start_date == set_of_tasks_data['task1'].start_date

        end_date = convert_date_class_to_iso_format(task.end_date)
        assert end_date != data['end_date']

        assert task.user.username == acc['username']
