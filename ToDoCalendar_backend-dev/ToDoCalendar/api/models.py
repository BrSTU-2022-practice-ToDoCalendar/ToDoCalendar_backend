from django.db import models


class User(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    Start_date = models.DateTimeField(auto_now_add=True)
    End_date = models.DateTimeField(auto_now_add=True)
