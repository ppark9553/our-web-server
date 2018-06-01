'''
****** TASK MANAGER USING FABRIC/PYTHON ******

RUN: "fab <taskname>"
(ex) fab shell
(the tasknames are defined below, check the codes below for more information)

###### LOCAL FAB TASKS ######
==> can run on local computer/servers
shell
runserver
static
new_static
migrate
test
lazy_commit
server_reload
restart_celery
js_gobble_reinstall
clean_known_hosts

###### OPEN SHELL TASKS ######
==> opens up shell as user: arbiter, in this case
init_web_shell
init_db_shell
init_cache_shell
init_gateway_shell
init_gobble_shell
init_mined_shell
root_web_shell
root_db_shell
root_cache_shell
root_gateway_shell
root_gobble_shell
root_mined_shell
web_shell
db_shell
cache_shell
gateway_shell
gobble_shell
mined_shell

###### INITIAL DEPLOY TASKS ######
init_servers

###### SERVER SPECIFIC TASKS ######
monitor_redis
'''

from fabric.api import *
from fab_settings import *

from autoserver.common import server_init
from autoserver.web import deploy_web

# variables here are defined in fab_settings.py
env.hosts = [
    local_ip,
    root_web,
    root_db,
    root_cache,
    root_gateway,
    root_gobble,
    root_mined,
    arbiter_web,
    arbiter_db,
    arbiter_cache,
    arbiter_gateway,
    arbiter_gobble,
    arbiter_mined
]

# set passwords for each hosts defined above
env.passwords = {
    local_ip: '',
    root_web: web_pw,
    root_db: db_pw,
    root_cache: cache_pw,
    root_gateway: gateway_pw,
    root_gobble: gobble_pw,
    root_mined: mined_pw,
    arbiter_web: arbiter_pw,
    arbiter_db: arbiter_pw,
    arbiter_cache: arbiter_pw,
    arbiter_gateway: arbiter_pw,
    arbiter_gobble: arbiter_pw,
    arbiter_mined: arbiter_pw
}


###### LOCAL FAB TASKS ######
@task
@hosts(local_ip)
def shell():
    # opens the shell
    local('python manage.py shell')

@task
@hosts(local_ip)
def runserver():
    # runs the Django server
    local('python manage.py runserver')

@task
@hosts(local_ip)
def static():
    # collects static files again
    local('python manage.py collectstatic')

@task
@hosts(local_ip)
def new_static():
    # removes static-dist directory and collects static again
    local('rm -r static-dist')
    local('mkdir static-dist')
    local('python manage.py collectstatic')

@task
@hosts(local_ip)
def migrate():
    # make migrations on DB then migrate those changes
    local('python manage.py makemigrations')
    local('python manage.py migrate')

@task
@hosts(local_ip)
def test():
    # perform Django tests
    local('python manage.py test')

@task
@hosts(local_ip)
def lazy_commit():
    # git add . > git commit then git pushes changes lazily
    with settings(warn_only=True):
        local('git add .')
        local('git commit -m "commiting lazily: minor change only"')
    local('git push')

@task
@hosts(local_ip)
def server_reload():
    # local server reload
    local('sudo systemctl restart uwsgi')
    local('sudo systemctl restart nginx')

@task
@hosts(local_ip)
def restart_celery():
    # local celery/celerybeat restart
    # first migrates all changes
    execute(migrate)
    local('sudo supervisorctl restart arbiter_celery')
    local('sudo supervisorctl restart arbiter_celerybeat')

@task
@hosts(local_ip)
def js_gobble_reinstall():
    # reinstalls js-gobble app
    local('rm -r /home/arbiter/js-gobble')
    local('sudo bash /home/arbiter/buzzz/js-gobble/setup.sh')

@task
@hosts(local_ip)
def clean_known_hosts():
    # for mac users
    # delete all known host records
    local('echo "" > /Users/abc/.ssh/known_hosts')


###### OPEN SHELL TASKS ######
@task
@hosts(root_web)
def init_web_shell():
    env.password = web_pw
    open_shell()

@task
@hosts(root_db)
def init_db_shell():
    env.password = db_pw
    open_shell()

@task
@hosts(root_cache)
def init_cache_shell():
    env.password = cache_pw
    open_shell()

@task
@hosts(root_gateway)
def init_gateway_shell():
    env.password = gateway_pw
    open_shell()

@task
@hosts(root_gobble)
def init_gobble_shell():
    env.password = gobble_pw
    open_shell()

@task
@hosts(root_mined)
def init_mined_shell():
    env.password = mined_pw
    open_shell()

@task
@hosts(root_web)
def root_web_shell():
    env.password = root_pw
    open_shell()

@task
@hosts(root_db)
def root_db_shell():
    env.password = root_pw
    open_shell()

@task
@hosts(root_cache)
def root_cache_shell():
    env.password = root_pw
    open_shell()

@task
@hosts(root_gateway)
def root_gateway_shell():
    env.password = root_pw
    open_shell()

@task
@hosts(root_gobble)
def root_gobble_shell():
    env.password = root_pw
    open_shell()

@task
@hosts(root_mined)
def root_mined_shell():
    env.password = root_pw
    open_shell()

@task
@hosts(arbiter_web)
def web_shell():
    env.password = arbiter_pw
    open_shell()

@task
@hosts(arbiter_db)
def db_shell():
    env.password = arbiter_pw
    open_shell()

@task
@hosts(arbiter_cache)
def cache_shell():
    env.password = arbiter_pw
    open_shell()

@task
@hosts(arbiter_gateway)
def gateway_shell():
    env.password = arbiter_pw
    open_shell()

@task
@hosts(arbiter_gobble)
def gobble_shell():
    env.password = arbiter_pw
    open_shell()

@task
@hosts(arbiter_mined)
def mined_shell():
    env.password = arbiter_pw
    open_shell()


###### INITIAL DEPLOY TASKS ######
@task
@hosts(env.hosts[1:7])
def init_servers():
    server_init()


###### SERVER SPECIFIC TASKS ######
@task
@hosts(root_cache)
def monitor_redis():
    env.password = root_pw
    run('redis-cli -a da56038fa453c22d2c46e83179126e97d4d272d02ece83eb83a97357e842d065 monitor')
