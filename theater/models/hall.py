# the hall model
from theater.extensions import db
from theater.models import Model


class Hall(db.Model,Model):
    h_id = db.Column(db.Integer,primary_key=True)
    c_id = db.Column(db.Integer)
    h_name = db.Column(db.String(64),nullable=False)
    h_screen_type = db.Column(db.String(32))
    h_audio_type = db.Column(db.String(32))
    h_seats_num = db.Column(db.Integer,default=0,nullable=False)
    h_status = db.Column(db.Integer,
                         server_default='0',
                         nullable=False,
                         index=True)