import os


class NoneConfig(object):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_DEFAULT_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(NoneConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_PROD_URI')


class DevelopmentConfig(NoneConfig):
    DEBUG = 1
