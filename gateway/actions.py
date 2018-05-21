'''
The GatewayAction class defines all actions you throw to your gateway server

This works very much like how Javascript Redux library works.

How to use:

1. initialize GatewayAction instance
2. pass in a 'action_type' on construct
3. throw at GatewayStoreView in gateway/views.py --> the store will handle all actions
'''

class GatewayActionOBJ(object):

    def __init__(self, action_type):

        if action_type == 'MASS_DATE_CRAWL':
            self.ACTION = {
                'type': 'MASS_DATE_CRAWL',
                'reduce': 'mass_date_crawl',
                'cached_data': 'False'
            }

        elif action_type == 'MASS_DATE_SAVE':
            self.ACTION = {
                'type': 'MASS_DATE_SAVE',
                'reduce': 'mass_date_save',
                'cached_data': 'True',
                'saved-at': 'db',
                'cache-key': 'mass_date',
                'parameter-type': type([])
            }

        else:
            self.ACTION = {
                'type': 'None'
            }
