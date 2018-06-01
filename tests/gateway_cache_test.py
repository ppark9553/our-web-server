import os, sys, glob

start_path = os.getcwd()
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbiter.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

### test script ###
import pandas as pd

from gateway.cache import RedisClient

def testCache():
    print('Test cache can create instance')
    r = RedisClient()
    print(r.redis_client)
    print('==========')

    print('Test cache can set key')
    res = r.set_key('pythontest', 'testing set key with python client')
    print(res)
    print('==========')

    print('Test cache can get key')
    res = r.get_key('pythontest')
    print(res)
    print('==========')

    print('Test cache can check for key existence')
    res = r.key_exists('pythontest')
    print(res)
    print('==========')

    print('Test cache can delete key')
    res = r.del_key('pythontest')
    print(res)
    print('==========')

    print('Test cache can set list')
    listdata = ['pythonlisttest', 1, 2, 3, 4, 5]
    if r.key_exists('pythonlisttest'):
        r.del_key('pythonlisttest')
    res = r.set_list(listdata)
    print(res)
    print('==========')

    print('Test cache can set list of string values')
    listdata2 = ['pythonlisttest2', 'a', 'b', 'c', 'd']
    if r.key_exists('pythonlisttest2'):
        r.del_key('pythonlisttest2')
    res = r.set_list(listdata2)
    print(res)
    print('==========')

    print('Test cache can get list')
    res = r.get_list('pythonlisttest', 'int')
    print(res)
    print('==========')

    print('Test cache can get list of string values')
    res = r.get_list('pythonlisttest2', 'str')
    print(res)
    print('==========')

    print('Test cache can set json')
    jsondata = {
        'key1': 1,
        'key2': 2,
        'keykey': {
            'keykey1': 1,
            'keykey2': 2
        }
    }
    if r.key_exists('pythonjsontest'):
        r.del_key('pythonjsontest')
    res = r.set_json('pythonjsontest', jsondata)
    print(res)
    print('==========')

    print('Test cache can get json')
    res = r.get_json('pythonjsontest')
    print(res)
    print(res['key1'])
    print(res['keykey']['keykey1'])
    print('==========')

    print('Test cache can set pd dataframe')
    df = pd.DataFrame([1, 2, 3, 4, 5])
    if r.key_exists('dftest'):
        r.del_key('dftest')
    res = r.set_df('dftest', df)
    print(res)
    print('==========')

    print('Test cache can get pd dataframe')
    res = r.get_df('dftest')
    print(res)
    print(res[0])
    print('==========')

### testing for django specific cache ###
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def testDjangoCache():
    print('Test cache can set value')
    cache.set('django_test', 'hello hello')
    print('==========')

    print('Test cache can get value')
    val = cache.get('django_test')
    print(val)
    print('==========')

testCache()
testDjangoCache()
