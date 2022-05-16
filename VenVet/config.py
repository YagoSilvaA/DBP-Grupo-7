import os
basedir = os.path.abspath(os.path.dirname(__file__))
# Correr estos 2 comandos para configurar la BD:
# export DATABASE_URL="postgresql://postgres:123456789@localhost/appointments"
# export APP_SETTINGS="config.DevelopmentConfig"

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'yyyyyyy'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True