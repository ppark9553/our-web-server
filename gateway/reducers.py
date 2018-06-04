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
)


class GatewayReducer(object):

    def __init__(self, action):
        self.logger = GatewayLogger()

        if action['type'] == 'GET_STATE':
            reducer = getattr(self, action['reduce'])
            self.reducer = reducer

        elif action['type'] == 'TEST':
            reducer = getattr(self, action['reduce'])
            self.reducer = reducer

        elif action['type'] == 'GET_WONSEOK_TEST':
            reducer = getattr(self, action['reduce'])
            self.reducer = reducer

        elif action['type'] == 'SAVE_WONSEOK_TEST':
            reducer = getattr(self, action['reduce'])
            self.reducer = reducer

        elif action['type'] == 'RESTART_TEST':
            reducer = getattr(self, action['reduce'])
            self.reducer = reducer

        elif action['type'] == 'ERROR_TEST':
            reducer = getattr(self, action['reduce'])
            self.reducer = reducer

        elif action['type'] == 'MASS_DATE_CRAWL':
            # get the reducer function with 'getattr' function
            reducer = getattr(self, action['reduce'])
            self.reducer = reducer

    def reduce(self):
        self.reducer()
        return True

    def get_state(self):
        print('get state')

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

    def mass_date_crawl(self):
        # send to js-gobble because crawling needs to use javascript
        mass_date_crawl.delay()

    def mass_date_save(self, save_at, cached_key):
        hostname = CONFIG['ip-address'][save_at]
        print('Hostname: {}'.format(hostname))
        r = redis.Redis(host=hostname, port=6379)
        print('Connected to Redis')
        mass_dates = r.lrange(cached_key, 0, -1)
        inst_list = []
        for date_data in mass_dates:
            date = date_data.decode('utf-8')
            date_inst = Date(date=date)
            inst_list.append(date_inst)
        Date.objects.bulk_create(inst_list)
        print('Date instances bulk created success')
        return True
