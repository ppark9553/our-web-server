from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arbiter.settings')
app = Celery('proj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

def add_task(task_name, task_func, task_cron, task_args):
    task_def = {
        'task': task_func,
        'schedule': task_cron,
        'args': task_args
    }
    app.conf.beat_schedule[task_name] = task_def

# base celerybeat scheduled programs here
app.conf.beat_schedule = {

}
