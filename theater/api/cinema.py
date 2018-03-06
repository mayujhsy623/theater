from flask import request

from theater.api import ApiView
from theater.extensions.validator import Validator
from theater.helper.code import Code
from theater.models.cinema import Cinema
from theater.models.hall import Hall
from theater.models.movie import Movie
from theater.models.play import Play
from theater.models.seat import Seat


class CinemaView(ApiView):
    def all(self):
        # get the information of all cinemas
        return Cinema.query.all()

    # the get route is defined specially, which need to visit '/cinema/?c_id=1'
    # put the '@Validator' before the function of 'get()' equals the statement 'get=Validator(get)'
    @Validator(c_id=int)
    def get(self):
        c_id = request.params['c_id']
        cinema = Cinema.get(c_id)
        if not cinema:
            return Code.cinema_does_not_exist,request.args
        return cinema

    @Validator(c_id=int)
    def halls(self):
        c_id = request.params['ci_id']
        cinema = Cinema.get(c_id)
        if not cinema:
            # '1' means the status code that been defined
            return Code.cinema_does_not_exist, {'c_id': c_id}
        cinema.halls = Hall.query.filter_by(c_id=c_id).all()
        return cinema

    @Validator(c_id=int)
    def plays(self):
        c_id = request.params['c_id']
        cinema = Cinema.get(c_id)
        if not cinema:
            return Code.cinema_does_not_exist, {'c_id': c_id}
        cinema.plays = Play.query.filter_by(c_id=c_id).all()
        if not cinema:
            return Code.cinema_does_not_exist, {'c_id': c_id}
        for play in cinema.plays:
            play.movies = Movie.get(play.m_id)
        return cinema

    @Validator(h_id=int)
    def seats(self):
        h_id = request.params['h_id']
        hall = Hall.query.get(h_id)
        if not hall:
            return Code.hall_does_not_exist, {'h_id': h_id}
        hall.seats = Seat.query.fliter_by(h_id=h_id).all()
        return hall
