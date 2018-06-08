'''
Reducers should be pure functions, they shouldn't be dependent on any other states,
but only the parameters that they receive.

Though a little different from Redux.js, the reducers in Gateway server
should function to reduce the data received as parameters.

Normally this would require saving the data to a Django DB server.
'''
import redis, requests
from raven.contrib.django.raven_compat.models import client

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from arbiter.config import CONFIG
from gateway.models import GatewayState
from gateway.logger import GatewayLogger
from stockapi.models import Date

from gobble.tasks import (
    test,
    restart_test,
    get_wonseok_test,
    save_wonseok_test,
    mass_date_crawl,
    mass_date_save,
)


class GatewayReducer(object):

    def __init__(self, action):
        self.action = action

    def reduce(self):
        reducer = getattr(self, self.action['reduce'])
        reducer()
        return True

    def get_state(self):
        print('get state')

    ##### TEST REDUCERS #####
    def test(self):
        test.delay()

    def get_wonseok_test(self):
        get_wonseok_test.delay()

    def save_wonseok_test(self):
        save_wonseok_test.delay()

    def restart_test(self):
        restart_test.delay()

    def error_test(self):
        # tests Sentry capture error
        try:
            2 / 0
        except ZeroDivisionError:
            client.captureException()
    ##### END TEST REDUCERS #####

    def mass_date_crawl(self):
        # send to js-gobble because crawling needs to use javascript
        try:
            mass_date_crawl.delay()
        except:
            client.captureException()

    def mass_date_save(self, save_at, cached_key):
        try:
            cache_key = self.action['cache_key']
            to = self.action['to']
            mass_date_save.delay(cache_key, to)
        except:
            client.captureException()
