from tests.hepler import FlaskTestBase


class TestApiPlay(FlaskTestBase):
    def test_play_seats(self):
        p_id = 1
        rv = self.get_succ_json('play/seats/', p_id=p_id)
        for seat in rv['data']:
            self.assertEqual(
                seat['p_id'],
                p_id
            )
