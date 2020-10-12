from os import path

BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


class ConfigurationBase:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigurationDevelopment(ConfigurationBase):
    DEBUG = True


class ConfigurationProduction(ConfigurationBase):
    DEBUG = False
