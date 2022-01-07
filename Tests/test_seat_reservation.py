from unittest import TestCase
from reservation import SeatReservation
import os


class TestSeatReservation(TestCase):
    def setUp(self):
        super().setUp()
        self.num_rows = 3
        self.num_cols = 2
        self.test_file = 'test_file.txt'
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.sr = SeatReservation(self.test_file, self.num_rows, self.num_cols)

    def test_validate_init_values(self):
        self.assertEqual(self.sr.rows, self.num_rows)
        self.assertEqual(self.sr.seats_per_row, self.num_cols)
        # self.assertEqual(len(self.sr.reservations), self.num_rows)
        # self.assertEqual(len(self.sr.reservations[0]), self.num_cols)
        # seat = self.sr.reservations[0][0]
        # self.assertFalse(seat.reserved)
        self.assertIsNone(self.sr.action)
        self.assertIsNone(self.sr.start_seat)
        self.assertIsNone(self.sr.num_consecutive_seats)
        # print(self.sr.reservations)
        # print(self.sr.reservations[0][0])
        print(self.sr.fds.read())

