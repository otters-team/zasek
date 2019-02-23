from pprint import pprint

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from zasek.api.models import Project, Task
from zasek.api.serializers import UserTaskSerializer, ProjectSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = UserTaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        tasks = Task.objects.filter(
            user=self.request.user.id,
            end__isnull=True,
        )
        tasks.update(
            end=timezone.now(),
        )
        super().perform_create(serializer)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        task = self.get_object()
        task.end = timezone.now()
        task.save()
        return Response({'status': 'ok'})


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
