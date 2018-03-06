from unittest import TestCase
from urllib.parse import urlencode

from flask import json

import theater
from theater.configs.test import TestConfig
from theater.helper.code import Code


class FlaskTestBase(TestCase):
    def setUp(self):
        """Creates the Flask application and the APIManager."""
        app = theater.create_app(TestConfig)
        app.logger.disabled = True
        self.flaskapp = app
        self.app = app.test_client()
        with app.app_context():
            from theater.extensions import db
            from theater.models.cinema import Cinema  # noqa
            from theater.models.hall import Hall  # noqa
            from theater.models.movie import Movie  # noqa
            from theater.models.play import Play  # noqa
            from theater.models.seat import Seat  # noqa
            from theater.models.seat import PlaySeat  # noqa
            from theater.models.order import Order  # noqa
            db.create_all()
            Cinema.create_test_data(cinema_num=1, hall_num=1, play_num=1)
            Movie.create_test_data()

    def assert_get(self, uri, assert_code, method='GET', **params):
        if method == 'POST':
            # send the request to the uri, the parameter is 'params'
            rv = self.app.post(uri, data=params)
        # send the ger request
        else:
            # if the request has parameter
            if params:
                # add the parameter after the uri, like: /cinema/get/?pid=1
                rv = self.app.get('%s?%s' % (uri, urlencode(params)))
            else:
                # no parameter request uri
                rv = self.app.get(uri)
        # assertEqual: assert will judge the tow parameters, if they are equal then keep running otherwise return fail
        self.assertEqual(rv.status_code, assert_code)
        return rv

    # to test whether the request is successful
    def get200(self, uri, method='GET', **params):
        return self.assert_get(uri, 200, method, **params)

    def get400(self, uri, method='GET', **params):
        return self.assert_get(uri, 400, method, **params)

    # to get the response objects and change them to json type
    def get_json(self, uri, method='GET', **params):
        rv = self.get200(uri, method, **params)
        return json.loads(rv.data)

    def get_succ_json(self, uri, method='GET', **params):
        data = self.get_json(uri, method, **params)
        self.assertEqual(data['rc'], Code.succ.value)
        return data
