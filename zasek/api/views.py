from datetime import datetime

import pytz
from dateutil import parser
from django.db.models import Sum
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from zasek.api.models import Project, Task
from zasek.api.serializers import UserTaskSerializer, ProjectSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = UserTaskSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'task_number',
        'project_id',
        'user_id',
    )

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

    @action(detail=True, methods=['get'])
    def close(self, request, pk=None):
        task = self.get_object()
        task.end = timezone.now()
        duration_timedelta = task.end - task.start
        if duration_timedelta.days:
            task.task_duration = duration_timedelta.days * 60 * 60 * 24
        task.task_duration += duration_timedelta.seconds
        task.save()
        return Response({'status': 'ok'})

    @action(detail=False, methods=['get'])
    def report(self, request):
        start_param = self.request.query_params.get('start', None)
        end_param = self.request.query_params.get('end', None)
        data = Task.objects
        if start_param:
            start = parser.parse(start_param).replace(tzinfo=pytz.utc)
            data = data.filter(start__gte=start)
        if end_param:
            end = parser.parse(end_param).replace(tzinfo=pytz.utc)
            data = data.filter(end__lte=end)
        data = data.values('task_number', 'project_id').annotate(Sum('task_duration'))
        return Response(data)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
