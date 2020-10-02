class ConfigurationBase:
    SQLALCHEMY_DATABASE_URI = "sqlite:///sample.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigurationDevelopment(ConfigurationBase):
    DEBUG = True


class ConfigurationProduction(ConfigurationBase):
    DEBUG = False
