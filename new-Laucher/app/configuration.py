class Config(object):
    """
    Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class DevelopmentConfig(Config):
    """
    Development Configuration
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Testing Configuration
    """
    TESTING = True
