from theater.configs.default import DefaultConfig

# the setting of test
# to inherit the 'DefaultConfig'
class TestConfig(DefaultConfig):
    TESTING = True
    JSON_SORT_KEYS = False
    # to show the sql sentence
    SQLALCHEMY_ECHO = False
    # sqlite database, no need the address and run in the memory, the data will be cleaned after shut down
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
