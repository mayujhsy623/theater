from tests.hepler import FlaskTestBase


class TestApiCinema(FlaskTestBase):
    def test_cinema_index(self):
        self.get_succ_json('cinema/all/')

    def test_cinema_halls(self):
        self.get400('cinema/halls/')
        data = self.get_succ_json('cinema/halls/',c_id=1)
        self.assertIsNotNone(data['data'])

    def test_cinema_plays(self):
        self.get400('cinema/plays/')
        self.get_succ_json('cinema/plays/',c_id=1)