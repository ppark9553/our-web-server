'''
GatewayStateMachine app keeps track of all the app task states and status
for better maintenance of all tasks
'''

class GatewayStateMachine:
    # a singleton implementation of gateway state machine
    class __GatewayStateMachine:

        def __init__(self, state):
            self.current_state = state

        def __str__(self):
            return repr(self) + self.val

    instance = None

    def __init__(self, arg):
        if not GatewayStateMachine.instance:
            GatewayStateMachine.instance = GatewayStateMachine.__GatewayStateMachine(arg)
        else:
            GatewayStateMachine.instance.val = arg

    def __getattr__(self, name):
        return getattr(self.instance, name)
