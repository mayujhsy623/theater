from flask import request

from theater.api import ApiView
from theater.extensions.validator import Validator
from theater.models.movie import Movie


class MovieView(ApiView):
    def all(self):
        movies = list(Movie.query.all())
        return movies

    @Validator(m_id=int)
    def get(self):
        m_id = request.params['m_id']
        movie = Movie.get(m_id)
        return movie
