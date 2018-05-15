from fabric.api import *

@task
def shell():
    local('python manage.py shell')

@task
def runserver():
    local('python manage.py runserver')

@task
def static():
    local('python manage.py collectstatic')

@task
def migrate():
    local('python manage.py makemigrations')
    local('python manage.py migrate')

@task
def clean_db():
    with settings(want_only=True):
        local('python tools.py cleanmigrations')
    execute(migrate)

@task
def test():
    local('python manage.py test')

@task
def clean_db_and_test():
    execute(clean_db)
    execute(test)

@task
def lazy_commit():
    with settings(warn_only=True):
        local('git add .')
        local('git commit -m "commiting lazily: minor change only"')
    local('git push')

@task
def server_reload():
    local('sudo systemctl restart uwsgi')
    local('sudo systemctl restart nginx')

@task
def restart_celery():
    execute(migrate)
    local('sudo supervisorctl restart arbiter_celery')
    local('sudo supervisorctl restart arbiter_celerybeat')


# ### System Managin Tools ###
# from arbiter.config import CONFIG
#
# env.hosts = []
# for server_type, ip_address in CONFIG['ip-address'].items():
#     env.hosts.append(ip_address)
#
# @task
# def apply_changes():
#     execute(lazy_commit)
#     with cd('/home/arbiter/buzzz'):
#         run('git pull')
#         run('python manage.py makemigrations')
#         run('python manage.py migrate')
#         run('sudo systemctl restart uwsgi')
#         run('sudo systemctl restart nginx')
