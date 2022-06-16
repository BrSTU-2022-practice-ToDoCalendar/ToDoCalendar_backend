from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Task(models.Model):
    title = models.CharField(verbose_name='Заголовок задачи', max_length=256)
    description = models.TextField(
        verbose_name='Описание произведения',
        null=True,
        blank=True
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(
        User,
        verbose_name='Автор задачи',
        on_delete=models.CASCADE,
        related_name='tasks',
    )
