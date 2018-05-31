from fabric.api import cd, env, local, run, sudo, settings, put, open_shell
from fabric.contrib.files import exists

class Autoserver(object):
    '''
    Autoserver wraps up basic commands needed for deploying and managing Ubuntu (Debian based) servers.
    '''

    def __init__(self, project_name='', github_repo='', ip_address='', \
                 root_pw='', user_id='', user_pw='', db_id='', db_pw='', \
                 uwsgi_ini='', uwsgi_service='', nginx_conf='', \
                 supervisor_celery='', supervisor_celerybeat=''):
        # initialize Autoserver instance with github_repo, ip_address, root_pw, user_id, user_pw, db_id, and db_pw
        # uwsgi_ini, uwsgi_service, nginx_conf, supervisor_celery, supervisor_celerybeat data
        # you are most likely to get these data from config.py file
        self.PROJECT_NAME = project_name
        self.GITHUB_REPO = github_repo
        self.IP_ADDRESS = ip_address
        self.ROOT_PW = root_pw
        self.USER_ID = user_id
        self.USER_PW = user_pw
        self.DB_ID = db_id
        self.DB_PW = db_pw

        # configuration file names
        self.UWSGI_INI = uwsgi_ini
        self.UWSGI_SERVICE = uwsgi_service
        self.NGINX_CONF = nginx_conf
        self.SUPERVISOR_CELERY = supervisor_celery
        self.SUPERVISOR_CELERYBEAT = supervisor_celerybeat

        print(
        '''
        Project Name: {0}
        Github Repo: {1}
        IP Address: {2}
        Root PW: {3}
        User ID: {4}
        User PW: {5}
        DB ID: {6}
        DB PW: {7}

        UWSGI .ini file: {8}
        UWSGI .service file: {9}
        NGINX configuration file: {10}
        Supervisor celery file: {11}
        Supervisor celerybeat file: {12}
        '''.format(self.PROJECT_NAME,
                   self.GITHUB_REPO,
                   self.IP_ADDRESS,
                   self.ROOT_PW,
                   self.USER_ID,
                   self.USER_PW,
                   self.DB_ID,
                   self.DB_PW,
                   self.UWSGI_INI,
                   self.UWSGI_SERVICE,
                   self.NGINX_CONF,
                   self.SUPERVISOR_CELERY,
                   self.SUPERVISOR_CELERYBEAT
                   )
        )

    ### TEST PASSED ###
    def set_root_password(self):
        run('echo -e "{0}\n{1}" | passwd root'.format(self.ROOT_PW, self.ROOT_PW))
        return True # returns True after running so DeployTester knows that the function ran

    ### TEST PASSED ###
    def create_user(self):
        run('echo -e "{0}\n{1}" | adduser {2}'.format(self.USER_PW,
                                                      self.USER_PW,
                                                      self.USER_ID))
        run('usermod -aG sudo {}'.format(self.USER_ID))
        run('groups {}'.format(self.USER_ID))
        return True

    ### TEST PASSED ###
    def start_firewall(self):
        run('sudo ufw app list')
        run('sudo ufw allow OpenSSH')
        run('echo -e "y" | sudo ufw enable')
        return True

    ### TEST PASSED ###
    def update_and_download_dependencies(self):
        run('sudo apt-get update')
        run('sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib')
        return True

    ### TEST PASSED ###
    def setup_postgresql(self):
        # open port 5432 to remote computers/servers
        run('sudo ufw allow 5432')
        # moving postgresql configuration files to server
        # this is needed to allow access from remote computers to server
        put('./config/postgresql/postgresql.conf', '/etc/postgresql/9.5/main/postgresql.conf')
        put('./config/postgresql/pg_hba.conf', '/etc/postgresql/9.5/main/pg_hba.conf')
        # start, enable and restart postgresql service
        run('sudo systemctl start postgresql.service')
        run('sudo systemctl enable postgresql.service')
        run('sudo systemctl restart postgresql.service')

        # create database table and user if they do not exist already
        with settings(warn_only=True):
            run('sudo -i -u postgres psql -c "CREATE DATABASE {};"'.format(self.DB_ID))
        with settings(warn_only=True):
            run("sudo -i -u postgres psql -c \"CREATE USER {0} WITH PASSWORD '{1}';\"".format(self.DB_ID, self.DB_PW))
        run("sudo -i -u postgres psql -c \"ALTER ROLE {} SET client_encoding TO 'utf8';\"".format(self.DB_ID))
        run("sudo -i -u postgres psql -c \"ALTER ROLE {} SET default_transaction_isolation TO 'read committed';\"".format(self.DB_ID))
        run("sudo -i -u postgres psql -c \"ALTER ROLE {} SET timezone TO 'UTC';\"".format(self.DB_ID))
        run("sudo -i -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE {0} TO {1};\"".format(self.DB_ID, self.DB_ID))
        return True

    ### TEST PASSED ###
    def setup_python_virtualenv(self):
        # download dependencies
        run('sudo -H pip3 install --upgrade pip')
        run('sudo pip3 install setuptools')
        run('sudo -H pip3 install virtualenv virtualenvwrapper')
        # configure virtualenvwrapper to load on terminal open
        run('echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc')
        run('echo "export WORKON_HOME=/home/{}/venv" >> ~/.bashrc'.format(self.USER_ID))
        run('echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc')
        # final step of this is to reboot server
        run('source ~/.bashrc')
        return True

    ### TEST PASSED ###
    def pull_github_code(self):
        # create project folder to move your github code into
        with settings(warn_only=True):
            run('mkdir /home/{0}/{1}'.format(self.USER_ID, self.PROJECT_NAME))
        with cd('/home/{0}/{1}'.format(self.USER_ID, self.PROJECT_NAME)):
            run('git clone {}'.format(self.GITHUB_REPO)) # clone your github code
            repo_name = self.GITHUB_REPO.split('/')[-1].split('.')[0] # get your github repo name
            with settings(warn_only=True):
                # move your github repo code into your specified directory
                run('mv ./{0}/* /home/{1}/{2}'.format(repo_name,
                                                      self.USER_ID,
                                                      self.PROJECT_NAME))
                run('rm -r {}'.format(repo_name))
        return True

    def setup_nginx_uwsgi(self):
        # move all configuration files to server
        with settings(warn_only=True):
            run('mkdir /home/{}/config'.format(self.USER_ID))
        # move nginx conf file
        put('./config/nginx/{0}'.format(self.NGINX_CONF), \
            '/home/{0}/config/{1}'.format(self.USER_ID, self.NGINX_CONF))
        # move uwsgi conf files
        put('./config/uwsgi/{0}'.format(self.UWSGI_INI), \
            '/home/{0}/config/{1}'.format(self.USER_ID, self.UWSGI_INI))
        put('./config/uwsgi/{0}'.format(self.UWSGI_SERVICE), \
            '/home/{0}/config/{1}'.format(self.USER_ID, self.UWSGI_SERVICE))
        # install nginx and uwsgi on server
        # needs build-essential to compile uwsgi correctly, since it is run on a C++ platform
        run('sudo apt-get install build-essential nginx')
        run('sudo -H pip3 install uwsgi')
        # move uwsgi and nginx conf files from within the server to correct locations
        run('sudo mkdir -p /etc/uwsgi/sites')
        run('sudo cp /home/{0}/config/{1} /etc/nginx/sites-available/{2}'.format(self.USER_ID,
                                                                                 self.NGINX_CONF,
                                                                                 self.NGINX_CONF))
        with settings(warn_only=True):
            run('sudo ln -s etc/nginx/sites-available/{} /etc/nginx/sites-enabled'.format(self.NGINX_CONF))
        run('sudo nginx -t') # check for any errors in nginx conf file
        run('sudo systemctl restart nginx') # restart nginx to apply changes in configuration files
        run('sudo cp /home/{0}/config/{1} /etc/uwsgi/sites/{2}'.format(self.USER_ID,
                                                                       self.UWSGI_INI,
                                                                       self.UWSGI_INI))
        run('sudo cp /home/{0}/config/{1} /etc/systemd/system/{2}'.format(self.USER_ID,
                                                                                self.UWSGI_SERVICE,
                                                                                self.UWSGI_SERVICE))
        run('sudo systemctl start uwsgi')
        # enable both nginx and uwsgi
        run('sudo systemctl enable nginx')
        run('sudo systemctl enable uwsgi')
        # open firewall for port 80: nginx access
        run('sudo ufw allow "Nginx Full"')
        return True

    def send_django_config_file(self):
        # all sensitive data about our servers exist in the /config/django/config.py file
        # send the data over to your Django server
        put('./config/django/config.py', \
            '/home/{0}/{1}/{2}/config.py'.format(self.USER_ID,
                                                 self.PROJECT_NAME,
                                                 self.USER_ID))
        return True

    def setup_redis(self):
        run('sudo apt-get install redis-server')
        # open port 6379 to outside ssh connections
        run('sudo ufw allow 6379')
        # switch redis.conf file with the one used in Autoserver
        run('rm /etc/redis/redis.conf')
        put('./config/redis/redis.conf', '/etc/redis/redis.conf')
        run('sudo systemctl restart redis-server')
        return True

    def start_django_test_server_as_daemon(self):
        # first your virtualenv on the server needs to install all python dependencies
        # since accessing virtualenv with Fabric is difficult use 'open_shell'

        # 1. workon {projectname}
        # 2. pip install -r requirements.txt
        # 3. fab migrate
        if not exists('/home/{0}/venv/{1}/django-admin.py'.format(self.USER_ID, self.PROJECT_NAME)):
            with cd('/home/{0}/{1}'.format(self.USER_ID, self.PROJECT_NAME)):
                run('echo "install all Python dependencies and migrate"')
                open_shell()
        # intall Supervisor to daemonize uWSGI Django application
        run('sudo apt-get install supervisor')
        # move the Supervisor uwsgi.conf file to server
        put('./config/supervisor/uwsgi.conf', '/etc/supervisor/conf.d/uwsgi.conf')
        run('sudo supervisorctl reread')
        run('sudo supervisorctl update')
        run('sudo service supervisor start')
        # open port 8080
        run('sudo ufw allow 8080')
        return True
