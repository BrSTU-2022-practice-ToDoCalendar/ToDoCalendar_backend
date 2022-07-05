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
        assert Task.objects.get(id=id)


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

        tasks = Task.objects.filter(user__username=account['username'])

        assert response.status_code == status.HTTP_200_OK
        assert tasks.count() == len(response.data)

        for resp in response.data:
            task = tasks.get(id=resp['id'])

            assert (
                    convert_date_class_to_iso_format(task.start_date) ==
                    resp['start_date']
            )
            assert (
                    convert_date_class_to_iso_format(task.end_date) ==
                    resp['end_date']
            )
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

        second_account = set_of_authenticated_accounts_data[
            'authenticated_account2'
        ]
        second_user_tasks = Task.objects.filter(
            user__username=second_account['username']
        )

        assert response.status_code == status.HTTP_200_OK

        for resp in response.data:
            assert not second_user_tasks.filter(id=resp['id']).exists()

    @pytest.mark.django_db
    def test_list_task_with_year_param(
            self,
            client,
            set_of_authenticated_accounts_data,
    ):
        url = reverse('task-list')

        account = set_of_authenticated_accounts_data["authenticated_account1"]
        user = User.objects.get(username=account['username'])

        for i in range(10):
            Task.objects.create(
                title='task1',
                description='string1',
                start_date=f'201{i // 2}-08-24T14:15:22Z',
                end_date='2019-10-24T14:15:22Z',
                completed=False,
                user=user
            )

        auth_header = (
            'Bearer '
            f'{account["access-token"]}'
        )

        response = client.get(
            url,
            {'year': 2013},
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        for task in response.data:
            assert Task.objects.get(id=task['id']).start_date.year == 2013

    @pytest.mark.django_db
    def test_list_task_with_month_param(
            self,
            client,
            set_of_authenticated_accounts_data,
    ):
        url = reverse('task-list')

        account = set_of_authenticated_accounts_data["authenticated_account1"]
        user = User.objects.get(username=account['username'])

        for i in range(2, 12):
            Task.objects.create(
                title='task1',
                description='string1',
                start_date=f'2019-0{i // 2}-24T14:15:22Z',
                end_date='2019-10-24T14:15:22Z',
                completed=False,
                user=user
            )

        auth_header = (
            'Bearer '
            f'{account["access-token"]}'
        )

        response = client.get(
            url,
            {'month': 3},
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        for task in response.data:
            assert Task.objects.get(id=task['id']).start_date.month == 3

    @pytest.mark.django_db
    def test_list_task_with_day_param(
            self,
            client,
            set_of_authenticated_accounts_data,
    ):
        url = reverse('task-list')

        account = set_of_authenticated_accounts_data["authenticated_account1"]
        user = User.objects.get(username=account['username'])

        for i in range(2, 12):
            Task.objects.create(
                title='task1',
                description='string1',
                start_date=f'2019-08-0{i // 2}T14:15:22Z',
                end_date='2019-10-24T14:15:22Z',
                completed=False,
                user=user
            )

        auth_header = (
            'Bearer '
            f'{account["access-token"]}'
        )

        response = client.get(
            url,
            {'day': 3},
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        for task in response.data:
            assert Task.objects.get(id=task['id']).start_date.day == 3

    @pytest.mark.django_db
    def test_list_task_with_all_params(
            self,
            client,
            set_of_authenticated_accounts_data,
    ):
        url = reverse('task-list')

        account = set_of_authenticated_accounts_data["authenticated_account1"]
        user = User.objects.get(username=account['username'])

        for i in range(2, 10):
            Task.objects.create(
                title='task1',
                description='string1',
                start_date=f'201{i // 2}-0{i}-0{i}T14:15:22Z',
                end_date='2019-10-24T14:15:22Z',
                completed=False,
                user=user
            )

        auth_header = (
            'Bearer '
            f'{account["access-token"]}'
        )

        response = client.get(
            url,
            {'year': 2013, 'month': 6, 'day': 6},
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        task = Task.objects.get(id=response.data[0]['id'])
        assert task.start_date.year == 2013
        assert task.start_date.month == 6
        assert task.start_date.day == 6


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
    def test_correct_patch_completed_field_by_author(
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
            'completed': True,
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
        assert end_date == set_of_tasks_data['task1'].end_date

        assert task.completed == data['completed']

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

        task = Task.objects.get(id=id)

        assert task.title == set_of_tasks_data['task1'].title
        assert task.description == set_of_tasks_data['task1'].description
        start_date = convert_date_class_to_iso_format(task.start_date)
        assert start_date == set_of_tasks_data['task1'].start_date

        end_date = convert_date_class_to_iso_format(task.end_date)
        assert end_date != data['end_date']

        assert task.user.username == acc['username']

    @pytest.mark.django_db
    def test_correct_put_all_fields_by_author(
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
            'completed': False,
        }

        response = client.put(
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

        assert not task.completed

    @pytest.mark.django_db
    def test_correct_put_all_fields_by_another_user(
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
            'completed': False,
        }

        response = client.put(
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
    def test_correct_put_all_fields_by_unauthorized_user(
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
            'completed': False,
        }

        response = client.put(
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
    def test_invalid_put_all_fields_by_authorized_user(
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
            'completed': False,
        }

        response = client.put(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'].code == 'not_found'

    @pytest.mark.django_db
    def test_invalid_put_all_fields_with_same_startdate_enddate_by_author(
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
            'completed': True,
        }

        response = client.put(
            url,
            data=data,
            HTTP_AUTHORIZATION=auth_header,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        task = Task.objects.get(id=id)

        assert task.title != data['title']
        assert task.description != data['description']

        start_date = convert_date_class_to_iso_format(task.start_date)
        assert start_date != data['start_date']

        end_date = convert_date_class_to_iso_format(task.end_date)
        assert end_date != data['end_date']

        assert task.user.username == acc['username']


class TestStatusesTask:

    @pytest.mark.django_db
    def test_correct_statuses(
            self,
            client,
            set_of_authenticated_accounts_data,
    ):
        url = reverse('task-statuses')

        acc = set_of_authenticated_accounts_data['authenticated_account1']
        auth_header = f'Bearer {acc["access-token"]}'

        user = User.objects.get(username=acc['username'])

        Task.objects.create(title='task1', description='string1',
                            start_date='2019-10-01T14:15:22Z',
                            end_date='2019-10-24T14:15:22Z',
                            completed=False, user=user)
        Task.objects.create(title='task1', description='string1',
                            start_date='2019-10-01T14:15:22Z',
                            end_date='2019-10-24T14:15:22Z',
                            completed=False, user=user)

        Task.objects.create(title='task1', description='string1',
                            start_date='2019-10-02T14:15:22Z',
                            end_date='2019-10-24T14:15:22Z',
                            completed=False, user=user)
        Task.objects.create(title='task1', description='string1',
                            start_date='2019-10-02T14:15:22Z',
                            end_date='2019-10-24T14:15:22Z',
                            completed=True, user=user)

        Task.objects.create(title='task1', description='string1',
                            start_date='2019-10-03T14:15:22Z',
                            end_date='2019-10-24T14:15:22Z',
                            completed=True, user=user)
        Task.objects.create(title='task1', description='string1',
                            start_date='2019-10-03T14:15:22Z',
                            end_date='2019-10-24T14:15:22Z',
                            completed=True, user=user)

        response = client.get(
            url,
            HTTP_AUTHORIZATION=auth_header,
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

        assert response.data[0]['date'] == '2019-10-01T00:00:00Z'
        assert not response.data[0]['completed']
        assert response.data[0]['not_completed']

        assert response.data[1]['date'] == '2019-10-02T00:00:00Z'
        assert response.data[1]['completed']
        assert response.data[1]['not_completed']

        assert response.data[2]['date'] == '2019-10-03T00:00:00Z'
        assert response.data[2]['completed']
        assert not response.data[2]['not_completed']

    @pytest.mark.django_db
    def test_list_task_by_unauthorized_user(
            self,
            client,
    ):
        url = reverse('task-statuses')

        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'].code == 'not_authenticated'
