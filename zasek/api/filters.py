import django_filters
from django_filters.rest_framework import FilterSet

from zasek.api.models import Task


class TaskFilter(FilterSet):
    start__gte = django_filters.IsoDateTimeFilter(field_name='start', lookup_expr='gte')
    start__lte = django_filters.IsoDateTimeFilter(field_name='start', lookup_expr='lte')
    end__lte = django_filters.IsoDateTimeFilter(field_name='end', lookup_expr='lte')
    end__gte = django_filters.IsoDateTimeFilter(field_name='end', lookup_expr='gte')

    class Meta:
        model = Task
        fields = [
            'task_number',
            'project_id',
            'user_id',
            'start__gte',
            'start__lte',
            'end__lte',
            'end__gte',
        ]


class ReportFilter(FilterSet):
    start__gte = django_filters.IsoDateTimeFilter(field_name='start', lookup_expr='gte')
    start__lte = django_filters.IsoDateTimeFilter(field_name='start', lookup_expr='lte')
    end__lte = django_filters.IsoDateTimeFilter(field_name='end', lookup_expr='lte')
    end__gte = django_filters.IsoDateTimeFilter(field_name='end', lookup_expr='gte')

    class Meta:
        fields = [
            'start__gte',
            'start__lte',
            'end__lte',
            'end__gte',
        ]
