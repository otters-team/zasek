from django.conf import settings
from django.db import models


class Task(models.Model):

    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    task_number = models.IntegerField()
    description = models.CharField(max_length=150)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    task_duration = models.IntegerField(blank=True, default=0)
