import yaml

DEFAULT = """max_time_distance: 10
host: "0.0.0.0:7702"
timeout: 10
date_format: "%Y-%m-%d %H:%M:%S"
"""


def save_defaults():
    try:
        with open("config.yml", "w") as file:
            file.write(DEFAULT)
            return True
    except:
        return False


try:
    with open("config.yml", "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
except:
    save_defaults()
    config = yaml.load(DEFAULT, Loader=yaml.FullLoader)
