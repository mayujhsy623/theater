from theater import extensions

from flask import Flask
import logging
from logging import FileHandler, Formatter
from logging.handlers import SMTPHandler

from flask_redis import FlaskRedis

from theater.extensions import db, MockRedisWrapper
from theater.models import JSONEncoder
import os


# create the function of app
def create_app(config=None):
    app = Flask('theater')
    app.config.from_object('theater.configs.default.DefaultConfig')
    app.config.from_object(config)
    # try to update the config via the enivronment variable
    app.config.from_envvar('THEATER_SETTINGS', silent=True)
    configure_extensions(app)
    configure_views(app)
    # to execute the class of jsonencoder
    app.json_encoder = JSONEncoder

    if not app.debug:
        app.logger.setLevel(logging.INFO)
        mail_handler = SMTPHandler(
            app.config['EMAIL_HOST'],
            app.config['SERVER_EMAIL'],
            app.config['ADMINS'],
            'THEATER ALERT',
            credentials=(
                app.config['EMAIL_HOST_USER'],
                app.config['EMAIL_HOST_PASSWORD']))
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(Formatter(
            '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s
            
            Message:            %(message)s
            '''
        ))
        app.logger.addHandler(mail_handler)

        file_handler = FileHandler(os.path.join(app.config['LOG_DIR'], 'app,log'))
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
        ))
        app.logger.addHandler(file_handler)

    return app


def configure_extensions(app):
    db.init_app(app)
    # attention: when use the app.debug model, the data inside the redis will be abandoned by the server
    if app.debug or app.testing:
        extensions.redi = FlaskRedis.form_custom_provider(MockRedisWrapper)
    else:
        extensions.redi = FlaskRedis()
    extensions.redi.init_app(app)


def configure_views(app):
    for view in locals().values():
        if type(view) == type and issubclass(view, ApiView):
            view.register(app)
