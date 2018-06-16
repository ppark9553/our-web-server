import os, sys, glob

start_path = os.getcwd()
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbiter.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

### test script ###
from gateway.reducers import test_action

def testGatewayController():
    print('Test that reducer function gets properly decorated with gateway_reducer decorator')
    test_action()



testGatewayController()
