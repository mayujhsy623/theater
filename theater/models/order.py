from enum import Enum, unique
from random import randint

from sqlalchemy import text, func

from theater.extensions import db
from theater.helper import timeset
from theater.models import Model


@unique
class OrderStatus(Enum):
    locked = 1  # the seat been locked
    unlock = 2  # unlock the seat
    auto_unlock = 3  # the seat will be unlocked if there is no change in a certain time
    paid = 4
    printed = 5  # the ticket been printed
    refund = 6


class Order(db.Model, Model):
    __tablename__ = 'orders'
    # the id of the order
    o_id = db.Column(db.String(32), primary_key=True)
    c_id = db.Column(db.Integer, nullable=False)
    p_id = db.Column(db.Integer, nullable=False)
    s_id = db.Column(db.Integer, nullable=False)

    ticket_flag = db.Column(db.String(64))  # the code to get the tickets
    amount = db.Column(db.Integer, default=0, nullable=False)
    tickest_num = 0
    seller_order_num = db.Column(db.String(32), unique=True)
    paid_time = db.Column(db.DateTime)
    printed_time = db.Column(db.DateTime)
    refund_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_time = db.Column(db.DateTime, onupdate=func.now())
    status = db.Column(db.Integer, server_default='0', nullable=False)

    # to create an order
    @classmethod
    def create(cls, c_id, p_id, s_id):
        order = cls()
        # the order num: create time + 6 random number + p_id
        order.o_id = '%s%s%s' % (timeset.now(), randint(100000, 999999), p_id)
        order.c_id = c_id
        order.p_id = p_id
        # if there are more than one seats, then use list, and cut the list into string by ','
        # the string will be change to parameter list by the 'multi_int'
        if type(s_id) == list:
            order.s_id = ','.join(str(i) for i in s_id)
        else:
            order.s_id = s_id
        return order

    # to seek the order by the order num
    @classmethod
    def gen_ticket_flag(self):
        s = []
        for i in range(8):
            s.append(str(randint(1000, 9999)))
        self.ticket_flag = ''.join(s)

    def validate(self, ticket_flag):
        return self.ticket_flag == ticket_flag

    @classmethod
    def getby_orderno(cls, ordernum):
        return Order.query.filter_by(seller_order_num=ordernum).first()

    @classmethod
    def getby_ticket_flag(cls, ticket_flag):
        return cls.query.filter_by(ticket_flag=ticket_flag).first()
