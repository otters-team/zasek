from django.conf import settings
from django.db import models


class Task(models.Model):

    project_id = models.ForeignKey('Project', on_delete=models.CASCADE)
    task_number = models.IntegerField()
    description = models.CharField(max_length=150)
    start = models.DateTimeField(auto_now=True)
    end = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
