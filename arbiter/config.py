'''
This is the configuration file for our Django projects

Our Django projects can be used in many contexts, for instance:
we use our project in -> web, crawler, analysis contexts

This means that our configuration file should keep information on all the server settings

Since each server will hold different dependency issues and data,
define all such dependencies and data here

The dependency structure of Django is essential here.
Below are all the connections/dependencies we should take into account:

web <--> db/cache
db <--> gateway
gateway <--> gobble
gateway <--> mined

To visualize it more clearly:

web <--> db/cache <--> gateway <--> gobble
                               <--> mined
'''

CONFIG = {

    'common': {
        # Django settings variables
        'SECRET_KEY': '%-@*^al8d)z5cbetyfw1=%7h9b#t6=!-084y$@$74jugq3y0#6',
        'DB_NAME': 'arbiter',
        'DB_USER': 'arbiter',
        'DB_PW': 'makeitpopwe123arBITER!1',
        'AMQP_USER': 'arbiterbroker',
        'AMQP_PW': 'projectARgogo',
        'DEBUG': 'True',

        # general server variables
        'ROOT_PW': 'makeitpopwe123ARbiter;;',
        'USER_PW': 'projectargogo123alright;;',
        'CACHE_PW': 'da56038fa453c22d2c46e83179126e97d4d272d02ece83eb83a97357e842d065',

        # variables for deployment
        'PROJECT_NAME': 'buzzz',
        'GITHUB_REPO': 'https://github.com/ppark9553/our-web-server.git',
        'USER_ID': 'arbiter',
        'UWSGI_INI': 'buzzz.ini',
        'UWSGI_SERVICE': 'uwsgi.service',
        'NGINX_CONF': 'buzzz.conf',
        'SUPERVISOR_CELERY': 'celery.conf',
        'SUPERVISOR_CELERYBEAT': 'celerybeat.conf',
        'REDIS_CONF': 'redis.conf',

        'SENTRY_URL': 'https://19daa7122e0a4b6395ab8d15da36c8f3:d520ab25a8ed4c9aa4e8828b65f527fa@sentry.io/1228775'
    },

    'ip-address': {
        'local': '127.0.0.1',
        'web': '207.148.103.151',
        'db': '45.77.134.175', # deploy 1st: other servers need the database as dependency
        'cache': '202.182.113.123',
        'gateway': '149.28.25.177',
        'gobble': '149.28.18.34',
        'mined': '45.32.42.30'
    },

    'initial-deploy-pw': {
        'web': '4?BjP,TN]Gz.fGf,',
        'db': '4@Rb=ERy(},?UjD#',
        'cache': '3Y#faMd91)@)w%LK',
        'gateway': '(8tLXaZB]U+5@9=H',
        'gobble': 'Qt(5tTwsDD7raEAj',
        'mined': '{fR92qVn]drQb8hg'
    }

}

THIS_SYSTEM = 'web'
