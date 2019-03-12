from django.db.models import Sum
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from zasek.api.core import calc_task_duration
from zasek.api.filters import TaskFilter
from zasek.api.models import Project, Task
from zasek.api.serializers import ProjectSerializer, TaskReportSerializer, UserTaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = UserTaskSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer: Serializer):
        tasks = Task.objects.filter(
            user=self.request.user.id,
            end__isnull=True,
        )
        tasks.update(
            end=timezone.now(),
        )
        for task in tasks:
            task.task_duration = calc_task_duration(task)
            task.save()
        super().perform_create(serializer)

    @action(detail=True, methods=['post'])
    def close(self, request: Request, pk: int = None):
        task = self.get_object()
        task.end = timezone.now()
        task.task_duration = calc_task_duration(task)
        task.save()
        return Response(self.get_serializer(task).data)


class SummaryReportViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskReportSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = TaskFilter
    queryset = Task.objects.values('task_number', 'project_id').annotate(Sum('task_duration'))


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
