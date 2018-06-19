from gateway.controllers import gateway_reducer

from gateway.cache import RedisClient

@gateway_reducer
def test_action(**params):
    task_1 = params['task_1']
    testing_words = params['testing_words']

    print('running gobble.tasks.test_action function')
    print(testing_words)
    task_1()

@gateway_reducer
def mass_sd_crawl(**params):
    gobble_mass_sd_crawl = params['gobble_mass_sd_crawl']
    gobble_mass_sd_crawl.delay()

@gateway_reducer
def mass_sd_save(**params):
    gobble_mass_sd_save = params['gobble_mass_sd_save']
    data_date_cache_key = params['mass_sd_date']
    data_cache_key = params['data_cache_key']
    state_cache_key = params['state_cache_key']

    r = RedisClient()

    if r.key_exists(data_date_cache_key):
        data_date = r.get_key(data_date_cache_key)
