'''
Reducers should be pure functions, they shouldn't be dependent on any other states,
but only the parameters that they receive.

Though a little different from Redux.js, the reducers in Gateway server
should function to reduce the data received as parameters.

Normally this would require saving the data to a Django DB server.
'''
import redis, requests

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from arbiter.config import CONFIG
from gateway.models import Gateway
from stockapi.models import Date


class GatewayReducer(object):

    def __init__(self, action):

        if action['type'] == 'MASS_DATE_SAVE':
            # get the reducer function with 'getattr' function
            reducer = getattr(self, action['reducer'])


    def mass_date_save(save_at, cached_key):
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
