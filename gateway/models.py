from django.db import models

STATE_TYPES = (
    ('P', 'Pass'),
    ('F', 'Fail'),
)


class GatewayAction(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20)

    def __str__(self):
        return '{} {}'.format(self.action, self.created)


class GatewayState(models.Model):
    date = models.CharField(max_length=10)
    task_name = models.CharField(max_length=20)
    state = models.CharField(max_length=1, choices=STATE_TYPES)
    log = models.CharField(max_length=50,
                           blank=True,
                           null=True)

    def __str__(self):
        return '{} {}'.format(self.date, self.table_name)
