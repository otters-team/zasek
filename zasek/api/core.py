from django.utils import timezone

from zasek.api.models import Task


def calc_task_duration(task: Task):
    task_duration = 0
    if task.end:
        duration_timedelta = task.end - task.start
    else:
        duration_timedelta = timezone.now() - task.start
    if duration_timedelta.days:
        task_duration = duration_timedelta.days * 60 * 60 * 24
    task_duration += duration_timedelta.seconds
    return task_duration
