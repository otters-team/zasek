from rest_framework import serializers
from zasek.api.models import Project, Task


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = (
            'prefix',
            'name',
        )


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    project_name = serializers.SerializerMethodField()
    task_duration = serializers.SerializerMethodField()

    def get_project_name(self, task: Task):
        return task.project.name

    def get_task_duration(self, task: Task):
        return task.end - task.start

    class Meta:
        model = Task
        fields = (
            'task_number',
            'description',
            'start',
            'end',
            'user',
        )
