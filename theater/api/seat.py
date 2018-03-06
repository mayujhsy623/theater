from datetime import datetime

from flask import request
from flask_classy import route

from theater.api import ApiView
from theater.extensions.validator import Validator, multi_int, multi_complex_int
from theater.helper.code import Code
from theater.models.order import Order, OrderStatus
from theater.models.play import Play
from theater.models.seat import PlaySeat


class SeatView(ApiView):
    # the API of seat, which include the id of the selected movie, the id of seat(can more than one ), the price, the order num
    @Validator(p_id=int, s_id=multi_int, price=int, ordernum=str)
    @route('/lock/', methods=['POST'])
    def lock(self):
        # to find the parameters of the seats from the 'request.params' of the 'try' of decorator
        p_id = request.params['p_id']
        s_id = request.params['s_id']
        price = request.params['price']
        ordernum = request.params['ordernum']
        # to find the play by p_id
        play = Play.get(p_id)
        # if cannot find the play in the database(the play is None)
        if not play:
            # return the status and the parameter
            return Code.play_does_not_exist, {'p_id': p_id}

        # if the price lower than the lowest price, return the status
        if price < play.lowest_price:
            return Code.price_less_than_the_lowest_price, {'price': price}

        # call the class function of 'lock' from the 'PlaySeat'
        # lock the seat that been selected, the 'locked_seats_num' is the return value of 'lock' function,the parameter inside 'lock()' is 'row'
        locked_seats_num = PlaySeat.lock(ordernum, p_id, s_id)

        # if the value of 'locked_seats_num(rows)' is 0, locked seat failed
        if not locked_seats_num:
            return Code.seat_lock_failed, {}

        # if the value is not 0, then create the order
        order = Order.create(play.c_id, p_id, s_id)
        order.seller_order_num = ordernum
        order.status = OrderStatus.locked.value
        order.tickest_num = locked_seats_num
        order.save()
        # return the value
        return {'locked_seats_num': locked_seats_num}

    @Validator(p_id=int, s_id=multi_int, ordernum=str)
    @route('/unlock/', methods=['POST'])
    def unlock(self):
        p_id = request.params['p_id']
        s_id = request.params['s_id']
        ordernum = request.params['ordernum']
        order = Order.getby_orderno(ordernum)
        if not order:
            return Code.order_does_not_exist, {'ordernum': ordernum}
        if order.status != OrderStatus.locked.value:
            return Code.order_status_error, {}
        unlocked_seat_num = PlaySeat.unlock(ordernum, p_id, s_id)
        if not unlocked_seat_num:
            return Code.seat_unlock_failed, {}
        order.status = OrderStatus.unlocked.value
        order.save()
        return {'unlocked_seats_num': unlocked_seat_num}

    @Validator(seats=multi_complex_int, ordernum=str)
    @route('/buy/', methods=['POST'])
    def buy(self):
        seats = request.params['seats']
        ordernum = request.params['ordernum']
        order = Order.getby_orderno(ordernum)
        if not order:
            return Code.order_does_not_exist, {'ordernum': ordernum}
        if order.status != OrderStatus.locked.value:
            return Code.order_status_error, {'ordernum': ordernum, 'status': order.status}
        order.seller_order_num = request.params['ordernum']

        # the amount of the order, if the amount does not exist equals to 0
        # a = a or b: a = a if a is empty, a = b
        order.amount = order.amount or 0
        s_id_list = []
        for s_id, handle_fee, price in seats:
            s_id_list.append(s_id)
            order.amount += handle_fee + price
        bought_seats_num = PlaySeat.buy(ordernum, order.p_id, s_id_list)
        if not bought_seats_num:
            return Code.seat_buy_failed, {}
        order.tickest_num = len(seats)
        order.paid_time = datetime.now()
        order.status = OrderStatus.paid.value

        # the inside function of order, to create a ticket code, which length is 32(the column should add 'unique')
        order.gen_ticket_flag()
        order.save()
        return {
            'bought_seats_num': bought_seats_num,
            'ticket_flag': order.ticket_flag
        }
