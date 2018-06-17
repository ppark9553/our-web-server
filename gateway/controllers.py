import time
from functools import wraps

from raven.contrib.django.raven_compat.models import client # Sentry
from django.utils.module_loading import import_string

from gateway.logger import GatewayLogger
from gateway.actions import ACTIONS

### Gateway specific exceptions ###
class NoParamTypesError(Exception):
    pass

class MatchParamTypeNumError(Exception):
    pass

class NoSuchParamTypeError(Exception):
    pass


class Controller:

    # you can only pass in str, int, float, function parameters to action reducers
    __param_types = ['str', 'int', 'float', 'function']

    def __init__(self, action_type):
        self.action = action_type

    def transform_action_definition_to_variables(self):
        action_dict = ACTIONS[self.action]
        # check if 'params' key exists and if existent,
        # create Controller instance attributes with the values
        if 'params' in action_dict.keys():

            ### RAISE ERROR ###
            # next check if 'param-types' is defined as a key in ACTIONS
            if 'param-types' not in action_dict.keys():
                raise NoParamTypesError('Need to define parameter types in key: "param-types"')

            params = action_dict['params']
            param_types = action_dict['param-types']

            ### RAISE ERROR ###
            # parameters should be transformed to variables
            if len(params.keys()) != len(param_types):
                error_msg = 'Parameter type number: {}, does not match, parameter number: {}'.format(len(param_types), len(params.keys()))
                raise MatchParamTypeNumError(error_msg)

            type_index = 0 # set index number so loop can access param_type
            # finally create parameters into class attributes
            for key, val in action_dict['params'].items():
                param_type = param_types[type_index] # get param type from list

                ### RAISE ERROR ###
                if param_type not in self.__class__.__param_types:
                    raise NoSuchParamTypeError('{} is not a viable parameter type option'.format(param_type))

                if param_type == 'function':
                    func = self._get_function_from_path(val)
                    # setting function as new method of class
                    setattr(self, key, func)
                elif param_type == 'str':
                    setattr(self, key, str(val))
                elif param_type == 'int':
                    setattr(self, key, int(val))
                elif param_type == 'float':
                    setattr(self, key, int(val))
                else:
                    setattr(self, key, val) # adding regular attributes

                type_index += 1

    def _get_function_from_path(self, path_in_string):
        func = import_string(path_in_string)
        return func

def gateway_reducer(reducer_function):
    # wrap reducer functions with Sentry error tracker
    # also track time for how long the task took
    @wraps(reducer_function)
    def sentry_enabled_reducer_function(*args, **kwargs):
        reducer_name = reducer_function.__qualname__
        task_name = reducer_name.upper()

        c = Controller(task_name)
        c.transform_action_definition_to_variables()

        kwargs = {}
        # change all dictionary key values to variables
        for key, val in c.__dict__.items():
            if key != 'action':
                kwargs[key] = val

        reduce_start_time = time.time()
        try:
            reducer_function(**kwargs)
        except:
            client.captureException() # capture error with Sentry
        reduce_end_time = time.time()
        took_time = reduce_end_time - reduce_start_time
        logger = GatewayLogger()
        logger.set_log(task_name, 'P', 'reducer {0} ran in {1} s'.format(reducer_name, took_time))
    return sentry_enabled_reducer_function


class GatewayActionOBJ:
    # check whether passed in action is available/defined
    def __init__(self, action_type):
        self.action_type = action_type
        if self.action_exists():
            self.ACTION = ACTIONS[action_type]
        else:
            self.ACTION = None

    def action_exists(self):
        # returns True is action already defined, else False
        if self.action_type in ACTIONS.keys():
            return True
        else:
            return False


class GatewayReducer:
    def __init__(self, action_obj):
        # action obj is GatewayActionOBJ instance
        self.action_obj = action_obj

        self.action = action_obj.ACTION # action dictionary
        self.reducing_app = self.action['reducing-app']
        self.reducer_name = action_obj.action_type # string value

    def reduce(self):
        # as of this moment, only gateway reducers can be ran
        if self.action['reducing-app'] == 'gateway':
            reducer = import_string('gateway.reducers.{}'.format(self.reducer_name))
            reducer()
            return True
        else:
            return False
