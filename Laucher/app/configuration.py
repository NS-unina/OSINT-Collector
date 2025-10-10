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
    TOOLS_DIRECTORY = "tools"


class TestingConfig(Config):
    """
    Testing Configuration
    """
    TESTING = True
    TOOLS_DIRECTORY = "tools"
