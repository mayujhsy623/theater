from datetime import datetime

from enum import Enum, unique
from sqlalchemy import text
from sqlalchemy.schema import Index

from theater.extensions import db
from theater.models import Model


@unique
class SeatStatus(Enum):
    ok = 0
    locked = 1
    sold = 2
    printed = 3
    booked = 9
    repair = 99


@unique
class SeatType(Enum):  # different seat type
    road = 0
    single = 1
    couple = 2
    reserve = 3  # keep the seat
    disable = 4  # for disable people
    vip = 5
    shake = 6


# the information of the seat
class Seat(db.Model, Model):
    # every record means one seat
    s_id = db.Column(db.Integer, primary_key=True)
    c_id = db.Column(db.Integer, nullable=False)
    h_id = db.Column(db.Integer, nullable=False)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    row = db.Column(db.String(8))
    column = db.Column(db.String(8))
    area = db.Column(db.String(8))
    love_seats = db.Column(db.String(32))
    seat_type = db.Column(db.String(16))
    status = db.Column(db.Integer, nullable=False, server_default='0')

    @classmethod
    def getby_hid(cls, h_id):
        return cls.query.filter_by(h_id=h_id).all()


# the play seat information
class PlaySeat(db.Model, Model):
    p_sid = db.Column(db.Integer, primary_key=True)
    order_num = db.Column(db.String(32), index=True)
    s_id = db.Column(db.Integer, nullable=False)
    p_id = db.Column(db.Integer, nullable=False)
    c_id = db.Column(db.Integer, nullable=False)
    h_id = db.Column(db.Integer, nullable=False)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    row = db.Column(db.String(8))
    column = db.Column(db.String(8))
    area = db.Column(db.String(8))
    love_seats = db.Column(db.String(32))
    seat_type = db.Column(db.String(16))
    status = db.Column(db.Integer,
                       nullable=False,
                       server_default='0',
                       index=True)
    locked_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))

    @classmethod
    def getby(cls, p_id, s_id):
        return cls.get('%s-%s' % (p_id, s_id))

    def copy(self, seat):
        # just copy the information of seat to the PlaySeat

        self.s_id = seat.s_id
        self.c_id = seat.c_id
        self.h_id = seat.h_id
        self.x = seat.x
        self.y = seat.y
        self.row = seat.row
        self.column = seat.column
        self.area = seat.area
        self.loev_seats = seat.love_seats
        self.seat_type = seat.seat_type
        self.status = seat.status

    @classmethod
    def getby_ordernum(cls, ordernum):
        cls.query.filter_by(ordernum=ordernum).all()
        return

    @classmethod
    def lock(cls, ordernum, p_id, s_id_list):
        # create the session of database
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter(
            PlaySeat.p_id == p_id,
            PlaySeat.status == SeatStatus.ok.value,
            PlaySeat.s_id.in_(s_id_list)
            # change the attribute of the seats: seller order num, status code and the locked time
        ).update(
            {'ordernum': ordernum,
             'status': SeatStatus.locked.value,
             'locked_time': datetime.now()},
            synchronize_session=False)  # means when update the database, other request will not be obstructed

        # after update, the database will return a value to show how many data are changed, if the value is 0, then the update failed
        if rows != len(s_id_list):
            session.rollback()
            return 0

        session.commit()
        return rows

    # unlock the seat
    @classmethod
    def unlock(cls, ordernum, p_id, s_id_list):
        session = db.create_scoped_session()
        # 'rows' is the return value comes from the database
        # the seat is seeked by order number and status, and change the seller order num to empty, the status change to available
        rows = session.query(PlaySeat).filter_by(
            ordernum=ordernum, status=SeatStatus.locked.value).update(
            {
                'ordernum': None,
                'status': SeatStatus.ok.value
            },
            synchronize_session=False)
        if rows != len(s_id_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def print_tickets(cls, ordernum, p_id, s_id_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            ordernum=ordernum, status=SeatStatus.sold.value).update(
            {'status': SeatStatus.printed.value},
            synchronize_session=False)
        if rows != len(s_id_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def refund(cls, ordernum, p_id, s_id_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            ordernum=ordernum,
            status=SeatStatus.sold.value).update(
            {'status': SeatStatus.ok.value,
             'ordernum': None},
            synchronize_session=False)
        if rows != len(s_id_list):
            session.rollback()
            return 0
        session.commit()
        return rows
