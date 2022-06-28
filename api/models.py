from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Task(models.Model):
    title = models.CharField(verbose_name='title', max_length=255)
    description = models.TextField(verbose_name='description', blank=True, null=True)
    start_date = models.DateTimeField(verbose_name='start date')
    end_date = models.DateTimeField(verbose_name='end date')

    completed = models.BooleanField(default=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
