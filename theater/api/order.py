from datetime import datetime
from flask import request
from flask_classy import route

from theater.api import ApiView
from theater.extensions.validator import Validator, multi_int
from theater.helper.code import Code
from theater.models.movie import Movie
from theater.models.order import Order, OrderStatus
from theater.models.play import Play
from theater.models.seat import PlaySeat


class OrderView(ApiView):
    # the API of order
    @Validator(ordernum=str)
    def status(self):
        # to query the order status
        ordernum = request.params['ordernum']
        order = Order.getby_orderno(ordernum)
        if not order:
            return Code.order_does_not_exist, {"ordernum": ordernum}
        return {'status': order.status}

    @Validator(ordernum=str)
    def ticket(self):
        ordernum = request.params['ordernum']
        order = Order.getby_orderno(ordernum)
        if not order:
            return Code.order_does_not_exist, {'ordernum': ordernum}
        return {'ticket_flag': order.ticket_flag}

    @route('/ticket/info')
    @Validator(ordernum=str)
    # the get the information of the tickets
    def ticket_info(self):
        ordernum = request.params['ordernum']
        order = Order.getby_orderno(ordernum)
        if not order:
            return Code.order_does_not_exist, {'ordernum': ordernum}
        order.play = Play.get(order.p_id)
        order.movie = [Movie.get(order.play.m_id)]
        order.tickets = PlaySeat.getby_ordernum(ordernum)
        return order

    @route('/ticket/print', methods=['POST'])
    @Validator(ordernum=str, ticket_flag=str, s_id=multi_int)
    def print_ticket(self):
        seats = request.params['s_id']
        ticket_flag = request.params['ticket_flag']
        ordernum = request.params['ordernum']
        # to seek the order
        order = Order.getby_orderno(ordernum)
        # if the order does not exist
        if not order:
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already, {'status': order.status}
        if order.status != OrderStatus.paid.value:
            return Code.order_does_not_exist, {'status': order.status}
        # the ticket flag is wrong
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}
        # to execute the function and return the 'printed num', which means the number of the ticket
        printed_num = PlaySeat.print_tickets(order.seller_order_num, order.p_id, seats)
        if not printed_num:
            return Code.ticket_printed_failed, {}
        order.status = OrderStatus.printed.value
        order.printed_time = datetime.now()
        order.save()
        return {'printed_num': printed_num}

    @route('/ticket/refund', methods=['POST'])
    @Validator(ordernum=str, ticket_flag=str, s_id=multi_int)
    def refund_ticket(self):
        ordernum = request.params['ordernum']
        ticket_flag = request.params['ticket_flag']
        seats = request.params['s_id']
        # to seek the order
        order = Order.getby_orderno(ordernum)
        # when the order does not exist
        if not order:
            return Code.order_does_not_exist, {'ordernum': ordernum}
        # when the ticket is printed
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_failed, {}
        # when the ticket flag lost efficacy
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}
        # to execute the function, the 'refund_num' is the return value of the function
        refund_num = PlaySeat.refund(ordernum, order.p_id, seats)
        # when the refund num equals zero, refund failed
        if not refund_num:
            return Code.ticket_refund_failed, {}
        # change the status to 'refund already'
        order.status = OrderStatus.refund.value
        # add the refund time
        order.refund_time = datetime.now()
        order.save()
        return {'refund_num': refund_num}
