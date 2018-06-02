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
from gateway.cache import RedisClient
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
