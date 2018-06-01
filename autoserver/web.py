from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run, settings
from fabric.operations import open_shell

from autoserver.autoserver import Autoserver, BuzzzConfig

def deploy_web():
    buzzz = BuzzzConfig('web')
    config_obj = buzzz.get_conf()
    # deploys webserver using Autoserver instance with 'web' data
    autoserver = Autoserver(config_obj)
    autoserver.update()
    autoserver.set_root_password()
    with settings(warn_only=True):
        autoserver.create_user()
    autoserver.start_firewall()
    # autoserver.update_and_download_dependencies()
    # autoserver.setup_postgresql()
    # autoserver.setup_python_virtualenv()
    # # create virtualenv directly
    # if not exists('/home/{0}/venv/{1}'.format(autoserver.USER_ID, autoserver.PROJECT_NAME)):
    #     run('echo "Python virtualenv cannot be created with fabric, please type in (mkvirtualenv [project name])"')
    #     open_shell() # mkvirtualenv {project name}
    # autoserver.pull_github_code()
    # autoserver.setup_nginx_uwsgi()
    # autoserver.send_django_config_file()
    # # autoserver.start_django_test_server_as_daemon()
