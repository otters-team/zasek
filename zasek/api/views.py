from rest_framework import viewsets

from zasek.api.models import Project, Task
from zasek.api.serializers import UserTaskSerializer, ProjectSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = UserTaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user.id)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
