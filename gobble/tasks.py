from __future__ import absolute_import, unicode_literals
from celery.decorators import task

import random
import requests, json
from datetime import datetime
from fabric.api import local

from arbiter.config import CONFIG

@task(name="sum_two_numbers")
def add(x, y):
    return x + y

@task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total

@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)

@task(name="mass_date_crawl")
def mass_date_crawl():
    local('node /home/arbiter/js-gobble/test_script.js')

    gateway_ip = CONFIG['ip-address']['gateway']
    log_url = 'http://{}/hidden-api/gateway-states/'.format(gateway_ip)
    today_date = datetime.today().strftime('%Y%m%d')
    log_data = {
        'date': today_date,
        'task_name': 'mass_date_crawl',
        'state': 'P',
        'log': 'task: echo hello'
    }
    r = requests.post(log_url, data=log_data)
    return r.json()
