from flask_sqlalchemy import SQLAlchemy
from mockredis import MockRedis

db = SQLAlchemy()


class MockRedisWrapper(MockRedis):
    @classmethod
    def from_url(cls, *args, **kwargs):
        return cls()


redi = None
