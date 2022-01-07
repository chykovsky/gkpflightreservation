from unittest import TestCase
from reservation import SeatReservation


class TestSeatReservation(TestCase):
    def setUp(self):
        super().setUp()
        self.num_rows = 3
        self.num_cols = 2
        self.sr = SeatReservation('test_file.txt', self.num_rows, self.num_cols)

    def test_validate_init_values(self):
        self.assertEqual(self.sr.rows, self.num_rows)
        self.assertEqual(self.sr.seats_per_row, self.num_cols)
        self.assertEqual(len(self.sr.reservations), self.num_rows)
        self.assertEqual(len(self.sr.reservations[0]), self.num_cols)
        seat = self.sr.reservations[0][0]
        self.assertFalse(seat.reserved)
        self.assertIsNone(self.sr.action)
        self.assertIsNone(self.sr.start_seat)
        self.assertIsNone(self.sr.num_consecutive_seats)
        print(self.sr.reservations)

