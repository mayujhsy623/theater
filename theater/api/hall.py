from flask import request

from theater.api import ApiView
from theater.extensions.validator import Validator
from theater.helper.code import Code
from theater.models.hall import Hall
from theater.models.seat import Seat, SeatType


class HallView(ApiView):
    @Validator(h_id=int)
    def seats(self):
        h_id = request.params['h_id']
        hall = Hall.get(h_id)
        if not hall:
            return Code.hall_does_not_exist,{'h_id':h_id}
        hall.seats = Seat.query.filter(
            Seat.h_id == h_id,Seat.seat_type != SeatType.road.value
        ).all()
        return hall
