import requests

from arbiter.config import CONFIG

from gateway.logger import GatewayLogger


class TaskSender(object):

    def __init__(self, current_task):
        # first set logger
        self.logger = GatewayLogger()

        # define API endpoint
        self.gateway_ip = CONFIG['ip-address']['gateway']
        self.task_url = 'http://{}/hidden-api/task/?type='.format(self.gateway_ip)

        # needs current_task for loggin purposes
        self.current_task = current_task

    def send_task(next_task):
        # define API endpoint with new task name
        task_url = self.task_url + next_task
        # make API get request
        r = requests.get(task_url)
        reply = r.json()['status'] # status can return either of: DONE, FAIL, NO ACTION: ...
        if reply == 'DONE':
            this.logger.set_log(this.current_task, 'P', 'new task sent: {}'.format(next_task))
        elif reply == 'FAIL':
            this.logger.set_log(this.current_task, 'F', 'failed to send new task: {}'.format(next_task))
        elif 'NO ACTION' in reply:
            this.logger.set_log(this.current_task, 'F', 'no action called: {}'.format(next_task))
