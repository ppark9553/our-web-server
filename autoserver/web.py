from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run, settings
from fabric.operations import open_shell

from .autoserver import Autoserver
from .config import CONFIG

conf = CONFIG['web']

def deploy_webserver():
    # deploys webserver using Autoserver instance with 'web' data
    autoserver = Autoserver(conf['project-name'],
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
    autoserver.set_root_password()
    with settings(warn_only=True):
        autoserver.create_user()
    autoserver.start_firewall()
    autoserver.update_and_download_dependencies()
    autoserver.setup_postgresql()
    autoserver.setup_python_virtualenv()
    # create virtualenv directly
    if not exists('/home/{0}/venv/{1}'.format(autoserver.USER_ID, autoserver.PROJECT_NAME)):
        run('echo "Python virtualenv cannot be created with fabric, please type in (mkvirtualenv [project name])"')
        open_shell() # mkvirtualenv {project name}
    autoserver.pull_github_code()
    autoserver.setup_nginx_uwsgi()
    autoserver.send_django_config_file()
    # autoserver.start_django_test_server_as_daemon()
