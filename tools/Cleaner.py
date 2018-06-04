import os, glob

from arbiter.settings import INSTALLED_APPS


class Cleaner(object):
    def __init__(self, start_path):
        self.start_path = start_path
        self.apps = [app for app in INSTALLED_APPS if 'django' not in app and 'rest_framework' not in app and 'corsheaders' not in app]

        self.apps = self.apps + ['gobble']
        print(self.apps)

    def clean_migrations(self):
        for app in self.apps:
            os.chdir(self.start_path + '/' + app + '/migrations/')
            print(os.getcwd())
            mig_f = glob.glob('0*')
            for f in mig_f:
                print(f + ' deleted')
                os.remove(f)
