from rest_framework import serializers

from zasek.api.core import calc_task_duration
from zasek.api.models import Project, Task


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id',
            'prefix',
            'name',
        )


class UserTaskSerializer(serializers.HyperlinkedModelSerializer):
    project_name = serializers.SerializerMethodField()
    project_prefix = serializers.SerializerMethodField()
    task_duration = serializers.SerializerMethodField()

    project_id = serializers.IntegerField(write_only=True, required=True)

    def get_project_name(self, task: Task):
        return task.project.name

    def get_project_prefix(self, task: Task):
        return task.project.prefix

    def get_task_duration(self, task: Task):
        if not task.task_duration:
            return calc_task_duration(task)
        return task.task_duration

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Task
        fields = (
            'id',
            'project_id',
            'task_duration',
            'project_name',
            'project_prefix',
            'task_number',
            'description',
            'start',
            'end',
        )
