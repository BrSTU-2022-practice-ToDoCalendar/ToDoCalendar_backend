from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Task(models.Model):
    title = models.CharField('Title', max_length=255)
    description = models.TextField('Description',blank=True, null=True)
    start_date = models.DateTimeField('Start date')
    end_date = models.DateTimeField('End date')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
