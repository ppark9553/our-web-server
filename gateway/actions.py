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

        if action_type == 'GET_STATE':
            self.ACTION = {
                'type': 'GET_STATE',
                'reduce': 'get_state'
            }

        ###### TEST ACTIONS #######
        elif action_type == 'TEST':
            self.ACTION = {
                'type': 'TEST',
                'reduce': 'test'
            }

        elif action_type == 'GET_WONSEOK_TEST':
            self.ACTION = {
                'type': 'GET_WONSEOK_TEST',
                'reduce': 'get_wonseok_test',
                'cache-key': 'wonseok_test_from_local',
                'to': 'cache'
            }

        elif action_type == 'SAVE_WONSEOK_TEST':
            self.ACTION = {
                'type': 'SAVE_WONSEOK_TEST',
                'reduce': 'save_wonseok_test',
                'cache-key': 'wonseok_test_from_local',
                'from': 'cache'
            }

        elif action_type == 'RESTART_TEST':
            self.ACTION = {
                'type': 'RESTART_TEST',
                'reduce': 'restart_test'
            }

        elif action_type == 'ERROR_TEST':
            self.ACTION = {
                'type': 'ERROR_TEST',
                'reduce': 'error_test'
            }
        ###### END TEST ACTIONS ######

        elif action_type == 'MASS_DATE_CRAWL':
            self.ACTION = {
                'type': 'MASS_DATE_CRAWL',
                'reduce': 'mass_date_crawl',
                'reducing-app': 'gobble',
                'cached-data': '',
                'save': 'to:cache',
                'cache-key': 'mass_date',
                'parameter-type': []
            }

        elif action_type == 'MASS_DATE_SAVE':
            self.ACTION = {
                'type': 'MASS_DATE_SAVE',
                'reduce': 'mass_date_save',
                'reducing-app': 'gateway',
                'cached-data': 'True',
                'save': 'from:db',
                'cache-key': 'mass_date',
                'parameter-type': type([])
            }

        else:
            # add type 'None' so that StoreView can check for action type availability
            self.ACTION = {
                'type': 'None'
            }
