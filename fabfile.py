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

###### OPEN SHELL TASKS ######
==> opens up shell as user: arbiter, in this case
web_shell
db_shell
cache_shell
gateway_shell
gobble_shell
mined_shell
'''

from fabric.api import *
from fab_settings import *

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


###### OPEN SHELL TASKS ######
@task
@hosts(arbiter_web)
def web_shell():
    open_shell()

@task
@hosts(arbiter_db)
def db_shell():
    open_shell()

@task
@hosts(arbiter_cache)
def cache_shell():
    open_shell()

@task
@hosts(arbiter_gateway)
def gateway_shell():
    open_shell()

@task
@hosts(arbiter_gobble)
def gobble_shell():
    open_shell()

@task
@hosts(arbiter_mined)
def mined_shell():
    open_shell()
