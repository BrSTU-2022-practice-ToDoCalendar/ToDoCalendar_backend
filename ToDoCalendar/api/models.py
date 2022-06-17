from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Task(models.Model):
    title = models.CharField('Title', max_length=255)
    description = models.TextField('Description', blank=True)
    start_date = models.DateTimeField('Start date', auto_now_add=True)
    end_date = models.DateTimeField('End date', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)