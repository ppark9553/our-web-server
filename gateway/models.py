from django.db import models
from django.contrib.postgres.fields import JSONField

STATE_TYPES = (
    ('P', 'Pass'),
    ('F', 'Fail'),
)


class GatewayAction(models.Model):
    type = models.CharField(max_length=100)
    reduce = models.CharField(max_length=100)
    other = JSONField()

    def __str__(self):
        return self.type


class GatewayState(models.Model):
    date = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    task_name = models.CharField(max_length=50)
    state = models.CharField(max_length=1, choices=STATE_TYPES)
    log = models.TextField(blank=True,
                           null=True)

    def __str__(self):
        return '{} {}'.format(self.date, self.task_name)


class SoulLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    log = models.TextField()

    def __str__(self):
        return '{}'.format(self.log)
