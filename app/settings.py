# Some important settings parameters that can be set directlyin the code
from configparser import RawConfigParser as rawConf

# Configs parameters
conf = rawConf()
conf.read(r'config.txt')

# Filling parameters
SECRET_KEY = conf.get('neymo-config', 'SECRET_KEY')
MODULE = conf.get('neymo-config', 'MODULE')
CODE = conf.get('neymo-config', 'CODE')
