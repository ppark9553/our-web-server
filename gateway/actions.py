'''
The GatewayAction class defines all actions you can throw to your gateway server

This works very much alike to how Javascript Redux library works.

How to use:

1. initialize GatewayAction instance
2. pass in a 'action_type' on construct
3. throw at GatewayStoreView in gateway/views.py --> the store will handle all actions
'''

class GatewayAction(object):

    def __init__(self, action_type):

        if action_type == 'MASS_DATE_SAVE':
            self.ACTION = {
                'type': 'MASS_DATE_SAVE',
                'reduce': 'mass_date_save',
                'saved-at': 'db',
                'cache-key': 'mass_date',
                'parameter-type': type([])
            }
