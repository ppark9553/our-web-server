import requests, socket
from datetime import datetime

from arbiter.config import CONFIG


class GatewayLogger(object):

    def __init__(self):
        self.IP = socket.gethostbyname(socket.gethostname())
        # loggin destination: gateway url
        self.gateway_ip = CONFIG['ip-address']['gateway']
        self.log_url = 'http://{}/hidden-api/gateway-states/'.format(self.gateway_ip)

        # base data for logging: date
        self.date = datetime.today().strftime('%Y%m%d')

    def set_log(self, task_name, state, log):
        # set log data variables before saving log data
        self.task_name = task_name
        self.state = state # state should be either 'P' or 'F'
        self.log = '{0}: {1}'.format(self.IP, log)

        self._save_log()

    def _save_log(self):
        log_data = {
            'date': self.date,
            'task_name': self.task_name,
            'state': self.state,
            'log': self.log
        }
        r = requests.post(self.log_url, data=log_data)
