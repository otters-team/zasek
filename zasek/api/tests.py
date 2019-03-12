from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from zasek.api.models import Project, Task
from zasek.api.views import ProjectViewSet, TaskViewSet


class TasksTests(APITestCase):
    def test_create_task(self):
        user = User.objects.create_user(username='root', password='root')
        project_response = _create_project('economic', 'ecn', user)
        self.assertEqual(project_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().name, 'economic')

        task_response = _create_task(
            Project.objects.get().id,
            123,
            'some string for description',
            user,
        )
        self.assertEqual(task_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_close_task(self):
        user = User.objects.create_user(username='root', password='root')
        _create_project('economic', 'ecn', user)
        _create_task(
            Project.objects.get().id,
            123,
            'some string for description',
            user,
        )
        factory = APIRequestFactory()
        request = factory.post('/api/tasks/')
        force_authenticate(request, user=user)
        response = TaskViewSet.as_view({'post': 'close'})(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bool(Task.objects.get().end), not None)


def _create_project(name: str, prefix: str, user: User):
    factory = APIRequestFactory()
    request = factory.post(
        '/api/projects/',
        {
            "name": name,
            "prefix": prefix,
        },
        format='json'
    )
    force_authenticate(request, user=user)
    response = ProjectViewSet.as_view({'post': 'create'})(request)
    return response


def _create_task(project_id: int, task_number: int, description: str, user: User):
    factory = APIRequestFactory()
    request = factory.post(
        '/api/tasks/',
        {
            "project_id": project_id,
            "task_number": task_number,
            "description": description,
        },
        format='json',
    )
    force_authenticate(request, user=user)
    response = TaskViewSet.as_view({'post': 'create'})(request)
    return response
