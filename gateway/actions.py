ACTIONS = {
    # this is a test action to play around with, just leave it be for later reference purposes
    'TEST_ACTION': {
        'reducing-app': 'gateway',
        'params': {
            'task_1': 'gobble.tasks.test_action',
            'testing_words': 'this is a test text'
        },
        'param-types': ['function', 'str'],
    },

    ##### REAL TASKS BEGIN HERE #####
    'MASS_DATE_CRAWL': {
        'reducing-app': 'gateway',
        'params': {
            'data_cache_key': 'mass_date'
        },
        'param-types': ['str']
    },

    'MASS_DATE_SAVE': {
        'reducing-app': 'gateway',
        'params': {
            'data_cache_key': 'mass_date'
        },
        'param-types': ['str']
    },

    'MASS_SD_CRAWL': {
        'reducing-app': 'gateway',
        'params': {
            'gobble_mass_sd_crawl': 'gobble.tasks.mass_sd_crawl'
        },
        'param-types': ['function']
    },

    'MASS_SD_SAVE': {
        'reducing-app': 'gateway',
        'params': {
            'gobble_mass_sd_save': 'gobble.tasks.mass_sd_save',
            'data_date_cache_key': 'mass_sd_date',
            'data_cache_key': 'mass_sd',
            'state_cache_key': 'mass_sd_state'
        },
        'param-types': ['function']
    }

}
