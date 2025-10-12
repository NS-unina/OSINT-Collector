import os


class Config(object):
    """Configuration base, for all environments"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class DevelopmentConfig(Config):
    """Development Configuration"""
    DEBUG = True
    TOOLS_DIRECTORY = os.path.join(os.getcwd(), "tools")
    OUTOUT_DIRECTORY = os.path.join(os.getcwd(), "output")


class TestingConfig(Config):
    """Testing Configuration"""
    TESTING = True
    TOOLS_DIRECTORY = os.path.join(os.getcwd(), "tools")
    OUTOUT_DIRECTORY = os.path.join(os.getcwd(), "output")
