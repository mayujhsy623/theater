# the play model
from enum import unique, Enum

from sqlalchemy import text, func

from theater.extensions import db
from theater.models import Model


@unique
class PlayStatus(Enum):
    ok = 0
    repair = 99

class Play(db.Model,Model):
    p_id = db.Column(db.Integer,primary_key=True)
    c_id = db.Column(db.Integer,nullable=False)
    h_id = db.Column(db.Integer,nullable=False)
    m_id = db.Column(db.Integer,nullable=False)

    p_start_time = db.Column(db.DateTime,nullable=False)
    p_duration = db.Column(db.Integer,default=0,nullable=False)  # the duration of the film

    # the type of price: 1 means the original price, 2 means the discount price
    price_type = db.Column(db.Integer)
    price = db.Column(db.Integer)  # the original price, which is not necessary
    market_price = db.Column(db.Integer)  # the price that been sold at cinema
    lowest_price = db.Column(db.Integer,default=0)  # the lowest price that can be sold

    create_time = db.Column(db.DateTime,server_default=text('CURRENT_TIMESTAMP'))
    updated_time = db.Column(db.DateTime,onupdate=func.now())
    status = db.Column(db.Integer,
                       server_default='0',
                       nullable=False,
                       index=True)






