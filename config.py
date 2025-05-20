class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_PORT = 3306
    MYSQL_DB = 'healtrail_pharmacy'
    MYSQL_CURSORCLASS = 'DictCursor'
    SECRET_KEY = 'sdfsdfsdgsdewt4ww345gert34'

class DevelopmentConfig(Config):
    DEBUG = True

# class ProductionConfig(Config):
#     DEBUG = False

# class TestingConfig(Config):
#     TESTING = True
#     # Use a separate test database
#     MYSQL_DB = 'healtrail_pharmacy_test'
