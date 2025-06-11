from django.db import models


class Page(models.Model):
    title = models.TextField(default="page num 1")
