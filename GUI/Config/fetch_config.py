import os
from configparser import ConfigParser

config = ConfigParser()

if os.path.isfile('Config/config.ini'):
    config.read('Config/config.ini')
    print('config read')
else:
    config["SETTINGS"] = {
        'REGION': "LCK",
    }

    with open('Config/config.ini', 'w') as conf:
        config.write(conf)

    print('config created')
