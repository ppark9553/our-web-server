from __future__ import absolute_import, unicode_literals
from celery.decorators import task

import random
import requests, json
from datetime import datetime
from fabric.api import local

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from arbiter.config import CONFIG
from gateway.models import GatewayState
from gateway.cache import RedisClient
from gateway.logger import GatewayLogger
from gateway.task_sender import TaskSender

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

@task(name="test")
def test():
    task_name = 'TEST'
    logger = GatewayLogger()
    logger.set_log(task_name, 'P', 'gobble server received task: {}'.format(task_name))
    # test redis can set/get data
    r = RedisClient()
    r.set_key('TEST', 'testing gateway API data flow')
    res = r.get_key('TEST')
    logger.set_log(task_name, 'P', 'TEST 1: cache has key: {0}, with value: {1}'.format('TEST', res))
    cache.set('TEST2', 'testing Django cache set/get')
    res2 = cache.get('TEST2')
    logger.set_log(task_name, 'P', 'TEST 2: django cache has key: {0}, with value: {1}'.format('TEST2', res2))
    logger.set_log(task_name, 'P', 'COMPLETE')
    return True

@task(name="restart_test")
def restart_test():
    task_name = 'RESTART_TEST'
    logger = GatewayLogger()
    task_sender = TaskSender(task_name)

    logger.set_log(task_name, 'P', 'gobble server received task: {}'.format(task_name))

    # delete all TEST action related gateway logs
    GatewayState.objects.filter(task_name='TEST').delete()
    test_logs_num = GatewayState.objects.filter(task_name='TEST').count()
    if test_logs_num == 0:
        logger.set_log(task_name, 'P', 'deleted all TEST action related logs')

    # test redis can delete data
    r = RedisClient()
    res = r.del_key('TEST')
    if res == 1:
        logger.set_log(task_name, 'P', 'deleted key: {}'.format('TEST'))
    cache.delete('TEST2')
    logger.set_log(task_name, 'P', 'deleted key: {}'.format('TEST2'))
    # as a finishing touch retest TEST action by sending action
    task_sender.send_task('TEST')
    logger.set_log(task_name, 'P', 'COMPLETE')
    return True

@task(name="mass_date_crawl")
def mass_date_crawl():
    task_name = 'MASS_DATE_CRAWL'
    # log to gateway server
    logger = GatewayLogger() # initialize logger
    logger.set_log(task_name, 'P', 'gobble server received task: {}'.format(task_name))
    local('node /home/arbiter/js-gobble/{}.js'.format(task_name))
    logger.set_log(task_name, 'P', 'running "node /home/arbiter/js-gobble/{}.js"'.format(task_name))
    return True
