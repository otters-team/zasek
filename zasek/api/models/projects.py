from django.db import models


class Project(models.Model):

    prefix = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
