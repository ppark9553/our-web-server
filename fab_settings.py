from arbiter.config import CONFIG

# define IP addresses to use in fabfile
local_ip = CONFIG['ip-address']['local']
web_ip = CONFIG['ip-address']['web']
db_ip = CONFIG['ip-address']['web']
cache_ip = CONFIG['ip-address']['web']
gateway_ip = CONFIG['ip-address']['web']
gobble_ip = CONFIG['ip-address']['web']
mined_ip = CONFIG['ip-address']['web']

# define initial root password for initial server deploy
web_pw = CONFIG['initial-deploy-pw']['web']
db_pw = CONFIG['initial-deploy-pw']['db']
cache_pw = CONFIG['initial-deploy-pw']['cache']
gateway_pw = CONFIG['initial-deploy-pw']['gateway']
gobble_pw = CONFIG['initial-deploy-pw']['gobble']
mined_pw = CONFIG['initial-deploy-pw']['mined']
arbiter_pw = CONFIG['common']['USER_PW']

# define SSH connection destinations with users in front
root_web = 'root@{}'.format(web_ip)
root_db = 'root@{}'.format(db_ip)
root_cache = 'root@{}'.format(cache_ip)
root_gateway = 'root@{}'.format(gateway_ip)
root_gobble = 'root@{}'.format(gobble_ip)
root_mined = 'root@{}'.format(mined_ip)

arbiter_web = 'arbiter@{}'.format(web_ip)
arbiter_db = 'arbiter@{}'.format(db_ip)
arbiter_cache = 'arbiter@{}'.format(cache_ip)
arbiter_gateway = 'arbiter@{}'.format(gateway_ip)
arbiter_gobble = 'arbiter@{}'.format(gobble_ip)
arbiter_mined = 'arbiter@{}'.format(mined_ip)
