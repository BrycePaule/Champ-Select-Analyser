from GUI.Config.fetch_config import config

def set_region(region_code):
    settings = config['SETTINGS']
    settings['REGION'] = region_code
    write_config_changes()

def write_config_changes():
    with open('Config/config.ini', 'w') as conf:
        config.write(conf)