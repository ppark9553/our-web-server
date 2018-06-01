// configuration js object

CONFIG = {

    'common': {
        'SECRET_KEY': '%-@*^al8d)z5cbetyfw1=%7h9b#t6=!-084y$@$74jugq3y0#6',
        'DB_NAME': 'arbiter',
        'DB_USER': 'arbiter',
        'DB_PW': 'makeitpopwe123arBITER!1',
        'AMQP_USER': 'arbiterbroker',
        'AMQP_PW': 'dnqkrTJDRHD123ghkdlxld;;',
        'DEBUG': 'True',

        'ROOT_PW': 'makeitpopwe123ARbiter;;',
        'USER_PW': 'projectargogo123alright;;',
        'CACHE_PW': 'da56038fa453c22d2c46e83179126e97d4d272d02ece83eb83a97357e842d065',

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

    'ip': {
        'local': '127.0.0.1',
        'web': '207.148.103.151',
        'db': '45.77.134.175',
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

module.exports = CONFIG
