import os

import yaml


class Settings:
    main = None

    def __init__(self, filename='config.yml'):
        Settings.main = yaml.safe_load(open(os.path.join('config', filename)))