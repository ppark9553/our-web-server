from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run, settings

from .autoserver import Autoserver
from .config import CONFIG


class DeployTester:
    '''
    tests deployment without use of python unittest module
    keeps a counter of how many tests pass and fail
    since all tests will be run in a linear fashion, all tests must pass for Autoserver to work correctly

    Note: all method names to be tested should contain 'test' in the front of its method name,
    also, since test methods contain 'test' within their names, attributes should not user 'test'
    '''

    def __init__(self):
        # initialize tester with Autoserver instance
        conf = CONFIG['test'] # retrieve test server data from config.py
        self.autoserver = Autoserver(conf['project-name'],
                                     conf['github-repo'],
                                     conf['ip-address'],
                                     conf['root-pw'],
                                     conf['user-id'],
                                     conf['user-pw'],
                                     conf['db-id'],
                                     conf['db-pw'],

                                     conf['uwsgi-ini'],
                                     conf['uwsgi-service'],
                                     conf['nginx-conf'],
                                     conf['supervisor-celery'],
                                     conf['supervisor-celerybeat'])
        print('DeployTester instantiated, test start')

        self.passed_count = 0 # keep track of total passed tests count
        self.failed_status = False # change as soon as even one test fails

    def test_set_root_password(self):
        status = self.autoserver.set_root_password() # status will hold either True or nothing
        if status == True:
            self.passed_count += 1
            print('set_root_password successful')
        else:
            self.failed_status = True
            print('set_root_password failed')
        return self.passed_count, self.failed_status

    def test_create_user(self):
        status = ''
        with settings(warn_only=True):
            status = self.autoserver.create_user() # status will hold either True or nothing
        if status == True:
            self.passed_count += 1
            print('create_user successful')
        else:
            self.failed_status = True
            print('create_user failed')
        return self.passed_count, self.failed_status

    def test_start_firewall(self):
        status = self.autoserver.start_firewall() # status will hold either True or nothing
        if status == True:
            self.passed_count += 1
            print('start_firewall successful')
        else:
            self.failed_status = True
            print('start_firewall failed')
        return self.passed_count, self.failed_status

    def test_update_and_download_dependencies(self):
        status = self.autoserver.update_and_download_dependencies() # status will hold either True or nothing
        if status == True:
            self.passed_count += 1
            print('update_and_download_dependencies successful')
        else:
            self.failed_status = True
            print('update_and_download_dependencies failed')
        return self.passed_count, self.failed_status

    def test_setup_postgresql(self):
        status = self.autoserver.setup_postgresql() # status will hold either True or nothing
        if status == True:
            self.passed_count += 1
            print('setup_postgresql successful')
        else:
            self.failed_status = True
            print('setup_postgresql failed')
        return self.passed_count, self.failed_status

    def test_setup_python_virtualenv(self):
        status = self.autoserver.setup_python_virtualenv() # status will hold either True or nothing
        if status == True:
            self.passed_count += 1
            print('setup_python_virtualenv successful')
        else:
            self.failed_status = True
            print('setup_python_virtualenv failed')
        return self.passed_count, self.failed_status

    def test_pull_github_code(self):
        status = self.autoserver.pull_github_code() # status will hold either True or nothing
        if status == True:
            self.passed_count += 1
            print('pull_github_code successful')
        else:
            self.failed_status = True
            print('pull_github_code failed')
        return self.passed_count, self.failed_status

    def test_setup_nginx_uwsgi(self):
        status = self.autoserver.setup_nginx_uwsgi() # status will hold either True or nothing
        if status == True:
            self.passed_count += 1
            print('setup_nginx_uwsgi successful')
        else:
            self.failed_status = True
            print('setup_nginx_uwsgi failed')
        return self.passed_count, self.failed_status
