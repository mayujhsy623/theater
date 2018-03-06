# the cinema model
import random
import time

from datetime import datetime
import faker
import math

from flask import current_app

from theater.extensions import db
from theater.models import Model


class Cinema(db.Model, Model):
    c_id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(64), unique=True, nullable=False)  # the name must be unique and cannot be null
    c_address = db.Column(db.String(128), nullable=False)
    c_halls = db.Column(db.Integer, default=0, nullable=False)  # how many halls in the cinema
    c_handle_fee = db.Column(db.Integer, default=0, nullable=False)  # the service charge
    c_buy_limit = db.Column(db.Integer, default=0, nullable=False)  # how many tickets can be bought at one time
    status = db.Column(db.Integer, server_default='0', nullable=False, index=True)

    @classmethod
    def create_test_data(cls, cinema_num=10, hall_num=10, play_num=10):
        from theater.models.hall import Hall
        from theater.models.play import Play
        from theater.models.seat import PlaySeat, Seat
        from theater.models.order import Order
        f = faker.Faker()
        screen_type = [
            'normal',
            'IMAX'
        ]
        audio_type = [
            'normal',
            'Dolby'
        ]
        start_time = time.time()

        for i in range(1, cinenam_num + 1):
            cinema = Cinema()
            cinema.c_id = i
            cinema.c_name = '%s cinema' % f.street_name()
            cinema.c_address = f.address()
            cinema.status = 1
            cinema.save()

            for n in range(1, hall_num + 1):
                hall = Hall()
                hall.c_id = cinema.c_id
                hall.h_name = 'No %s hall' % n
                hall.h_screen_type = random.choice(screen_type)
                hall.h_audio_type = random.choice(audio_type)
                hall.h_seats_num = 25
                hall.status = 1
                hall.save()

                seats = []
                for s in range(1, hall.h_seats_num + 1):
                    seat = Seat()
                    seat.c_id = hall.c_id
                    seat.h_id = hall.h_id
                    seat.x = s % 5 or 5
                    seat.y = math.ceil(s / 5)
                    seat.row = seat.x
                    seat.column = seat.y
                    seat.seat_type = 1
                    seat.put()
                    seats.append(seat)
                Seat.commit()

                for p in range(1, play_num + 1):
                    play = Play()
                    play.c_id = cinema.c_id
                    play.h_id = hall.h_id
                    play.m_id = p
                    play.start_time = datetime.now()
                    play.p_duration = 3600
                    play.price_type = 1
                    play.price = 7000
                    play.market_price = 5000
                    play.lowest_price = 3000
                    play.status = 1
                    play.save()
                    for seat in seats:
                        ps = PlaySeat()
                        ps.p_id = play.p_id
                        ps.copy(seat)
                        ps.put()
                    PlaySeat.commit()
        current_app.logger.info('create test data done! cost %.2f seconds' % (time.time() - start_time))
