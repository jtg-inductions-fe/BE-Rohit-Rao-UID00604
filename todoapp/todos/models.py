from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone


class Todo(models.Model):
    NAME_MAX_LENGTH = 1000
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    done = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, default=None, null=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.done and self.date_completed is None:
            self.date_completed = timezone.now()
        super().save(*args, **kwargs)
