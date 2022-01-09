from unittest import TestCase
from reservation import SeatReservation, row_letter_index_map
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
        self.assertEqual(self.sr.filename, self.test_file)
        self.assertIsNotNone(self.sr.fds)
        self.assertIsNone(self.sr.action)
        self.assertIsNone(self.sr.start_seat)
        self.assertIsNone(self.sr.num_consecutive_seats)

    def test_row_letter_index_map(self):
        expected_num_rows = 20
        self.assertEqual(len(row_letter_index_map), expected_num_rows)
        self.assertEqual(row_letter_index_map['A'], 0)
