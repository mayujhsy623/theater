from tests.hepler import FlaskTestBase
from theater.helper.code import Code
from theater.models.seat import SeatStatus

p_id = 1
s_id_list = [1, 2]
s_id = ','.join([str(i) for i in s_id_list])
price = 5000
ordernum = 'test-%s-%s' % (p_id, s_id)


class TestApiSeat(FlaskTestBase):
    def test_seat1_lock(self):
        locked_seats_num = len(s_id_list)
        rv = self.get_succ_json(
            'seat/lock/',
            method='POST',
            p_id=p_id,
            price=price,
            s_id=s_id
        )
        self.assertEqual(rv['data']['locked_seats_num'], locked_seats_num)

        # confirm the seat has been changed
        rv = self.get_succ_json('play/seats/', p_id=p_id)
        succ_count = 0
        for seat in rv['data']:
            if seat['ordernum'] == ordernum:
                self.assertEqual(seat['status'], SeatStatus.locked.value)
                succ_count += 1
        self.assertEqual(succ_count, locked_seats_num)

        # to confirm the repetitive lock seat failed
        data = self.get_json(
            'seat/lock/',
            method='POST',
            ordernum='test-%s-%s' % (p_id, s_id),
            p_id=p_id,
            price=price,
            s_id=s_id
        )
        self.assertEqual(data['rc'], Code.seat_lock_failed.value)

    def test_seat2_unlock(self):
        seats_num = len(s_id_list)
        rv = self.get_succ_json(
            'seat/lock/',
            method='POST',
            ordernum=ordernum,
            p_id=p_id,
            price=price,
            s_id=s_id
        )
        self.assertEqual(rv['data']['locked_seats_num'], seats_num)
        rv = self.get_succ_json(
            'seat/unlock/',
            method='POST',
            ordernum='test-%s-%s' % (p_id, s_id),
            p_id=p_id,
            s_id=s_id
        )
        self.assertEqual(rv['data']['unlocked_seats_num'], seats_num)

        rv = self.get_succ_json('play/seats/', p_id=p_id)
        succ_count = 0
        for seat in rv['data']:
            if seat['s_id'] in s_id_list:
                self.assertEqual(seat['status'], SeatStatus.ok.value)
                succ_count += 1
        self.assertEqual(succ_count, seats_num)

    def test_seat3_buy(self):
        # lock the seat
        _ordernum = ordernum + 'buy'
        self.get_succ_json(
            'seat/lock/',
            method='POST',
            orderno=_ordernum,
            p_id=p_id,
            price=price,
            s_id=s_id)
        # then buy the ticket
        bought_seats_num = len(s_id_list)
        seats = ','.join(['%s-0-%s' % (i, price) for i in s_id_list])
        rv = self.get_succ_json(
            'seat/buy/',
            method='POST',
            ordernum=_ordernum,
            seats=seats
        )
