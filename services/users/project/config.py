# services/users/project/config.py

class BaseConfig:
    """Base Configuration"""
    TESTING = False

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    pass

class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True