from __future__ import absolute_import, unicode_literals
from celery.decorators import task

import random
import requests, json
from datetime import datetime
from fabric.api import local

from arbiter.config import CONFIG
from gateway.logger import GatewayLogger

# @task(name="sum_two_numbers")
# def add(x, y):
#     return x + y
#
# @task(name="multiply_two_numbers")
# def mul(x, y):
#     total = x * (y * random.randint(3, 100))
#     return total
#
# @task(name="sum_list_numbers")
# def xsum(numbers):
#     return sum(numbers)

@task(name="mass_date_crawl")
def mass_date_crawl():
    task_name = 'MASS_DATE_CRAWL'
    # log to gateway server
    logger = GatewayLogger() # initialize logger
    logger.set_log(task_name, 'P', 'gobble server received task: {}'.format(task_name))
    local('node /home/arbiter/js-gobble/{}.js'.format(task_name))
    logger.set_log(task_name, 'P', 'running "node /home/arbiter/js-gobble/{}.js"'.format(task_name))
    return True
