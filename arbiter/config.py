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
        'DB_PW': 'db76c15c05039965522afde9a3e09f076ddb44e6fa48b01c121ffc9793780039',
        'AMQP_USER': 'arbiterbroker',
        'AMQP_PW': '4d8ae8878bbb3da35ca2b35a52d57e3520df267ca4c6a8677a1cd4d58c2a78d8',
        'DEBUG': 'True',

        # general server variables
        'ROOT_PW': '6bf11c214d3481c681a83a948983e79233cac39150a64bdbc0a043f2d36d362f',
        'USER_PW': 'bc1504e8a4067f798fb1caed16ecf06716d37d883894e4df8709b7863f3c4368',
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
        'REDIS_CONF': 'redis.conf'
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
        'web': '9hJ@ax}b2[$f.6!R',
        'db': '6Q]oCM*VsH46EA-%',
        'cache': '3Y#faMd91)@)w%LK',
        'gateway': '+8HjS?3KXmKN6raW',
        'gobble': '1a_H)4,(1D-Jfg75',
        'mined': 'Jf9,SKAgJ7Y}6DWB'
    }

}

THIS_SYSTEM = 'web'
