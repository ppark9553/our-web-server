'''
This is the configuration file for our Django projects

Our Django projects can be used in many contexts, for instance:
we use our project in -> web, crawler, analysis contexts

This means that our configuration file should keep information on all the server settings

Since each server will hold different dependency issues and data,
define all such dependencies and data here,
and differentiate by changing the variable name: THIS_SYSTEM
THIS_SYSTEM should be set to either: 'web', 'db', 'gateway', 'gobble', 'mined'

The dependency structure of Django is essential here.
Below are all the connections/dependencies we should take into account:

web <--> db
db <--> gateway
gateway <--> gobble
gateway <--> mined

To visualize it more clearly:

web <--> db <--> gateway <--> gobble
                         <--> mined
'''

CONFIG = {

    'common': {
        'SECRET_KEY': '%-@*^al8d)z5cbetyfw1=%7h9b#t6=!-084y$@$74jugq3y0#6',
        'DB_NAME': 'arbiter',
        'DB_USER': 'arbiter',
        'DB_PW': 'projectAR!gogo',
        'AMQP_USER': 'arbiterbroker',
        'AMQP_PW': 'projectargogo',
        'DEBUG': 'True'
    },

    'web': {
        'IP_ADDRESS': '207.148.103.151'
    },

    'db': {
        'IP_ADDRESS': '45.77.134.175'
    },

    'gateway': {
        'IP_ADDRESS': '149.28.25.177'
    },

    'gobble': {
        'IP_ADDRESS': '149.28.18.34'
    },

    'mined': {
        'IP_ADDRESS': '45.32.42.30'
    }
}

THIS_SYSTEM = 'web'
