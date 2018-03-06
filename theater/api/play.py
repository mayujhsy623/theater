from flask import request

from theater.api import ApiView
from theater.extensions.validator import Validator
from theater.models.seat import PlaySeat, SeatType


class PlayView(ApiView):
    # return the information of available seats of selected 'Play'
    @Validator(p_id=int)
    def seats(self):
        return PlaySeat.query.filter(
            PlaySeat.p_id == request.params['p_id'],
            # seat_type=1 means the seat is locked
            # the type of seat is not equal to 'road'
            PlaySeat.seat_type != SeatType.road.value
        ).all()