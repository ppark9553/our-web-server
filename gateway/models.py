from django.db import models

STATE_TYPES = (
    ('P', 'Pass'),
    ('F', 'Fail'),
)


class GatewayState(models.Model):
    date = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    task_name = models.CharField(max_length=20)
    state = models.CharField(max_length=1, choices=STATE_TYPES)
    log = models.TextField(blank=True,
                           null=True)

    def __str__(self):
        return '{} {}'.format(self.date, self.task_name)
