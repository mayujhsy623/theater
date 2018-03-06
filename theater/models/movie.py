from flask import current_app

from theater.extensions import db
from theater.models import Model


class Movie(db.Model, Model):
    m_id = db.Column(db.Integer, primary_key=True)
    # sn is the code that create by The State Administration of Radio Film and Television of China
    sn = db.Column(db.String(32), unique=True, nullable=False)
    m_name = db.Column(db.String(64), nullable=False)
    m_language = db.Column(db.String(32))
    m_subtitle = db.Column(db.String(32))
    m_show_date = db.Column(db.Date)
    m_mode = db.Column(db.String(16))  # the type of movies like digital or film
    m_vision = db.Column(db.String(16))  # 2D or 3D
    m_screen_size = db.Column(db.String(16))
    m_introduction = db.Column(db.Text)
    m_status = db.Column(db.Integer,
                         server_default='0',
                         nullable=False,
                         index=True)

    @classmethod
    def create_test_data(cls, num=10):
        for i in range(1, num + 1):
            m = Movie()
            m.m_id = i
            m.sn = str(i).zfill(10)
            m.name = 'the name of movie is %s' % i
            m.m_language = 'English'
            m.m_subtitle = 'Mandarin'
            m.m_mode = 'digital'
            m.m_vision = '2D'
            m.m_screen_size = 'IMAX'
            m.m_introduction = 'hahaha'
            m.m_status = 1
            db.session.add(m)
        db.session.commit()
        current_app.logger.info('movie test data done!')
