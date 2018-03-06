from enum import Enum, unique


# the 'Code' had defined the different errors and their status code
@unique
class Code(Enum):
    succ = 0  # success
    required_parameter_missing = 100  # missing necessary parameter

    cinema_does_not_exist = 200
    hall_does_not_exist = 201

    play_does_not_exist = 300  # the movie does not exist
    price_less_than_the_lowest_price = 301

    seat_doest_not_exit = 400
    seat_already_locked = 401
    seat_not_locked_yet = 402
    seat_already_sold = 403
    seat_lock_failed = 404
    seat_unlock_failed = 405
    seat_bought_failed = 406

    order_does_not_exist = 500
    order_status_error = 501
    order_not_paid_yet = 502
    ticket_does_not_exist = 503
    ticket_printed_already = 504
    ticket_flag_error = 505
    ticket_printed_failed = 506
    ticket_refund_failed = 507
    
    unknown_error = 999
