from unittest import TestCase, mock
from reservation import SeatReservation
from datastore import FileDataStore
import os


class TestSeatReservation(TestCase):
    def setUp(self):
        super().setUp()
        self.num_rows = 5
        self.num_cols = 3
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
        expected_num_rows = 5
        expected_index_of_letter_a = 0
        expected_index_of_letter_c = 2
        self.assertEqual(len(self.sr.rll), expected_num_rows)
        self.assertEqual(self.sr.rll.index('A'), expected_index_of_letter_a)
        self.assertEqual(self.sr.rll.index('C'), expected_index_of_letter_c)

    @mock.patch("builtins.input", create=True)
    def test_service(self, mocked_input):
        mocked_input.side_effect = ["book a0 1", "quit"]
        try:
            self.sr.service()
            reservations = FileDataStore(self.test_file).read()
            seat = reservations[0][0]
            self.assertTrue(seat.reserved)
        except SystemExit:
            pass

    def test_process_action(self):
        self.sr.process_action("Book a0 1")

    @mock.patch("builtins.input", create=True)
    def test_run_once(self, mocked_input):
        mocked_input.side_effect = ["book a0 1"]
        self.sr.run_once()
        reservations = FileDataStore(self.test_file).read()
        seat = reservations[0][0]
        self.assertTrue(seat.reserved)

    @mock.patch("builtins.input", create=True)
    def test_run_once_not_reserved(self, mocked_input):
        mocked_input.side_effect = ["cancel a0 1"]
        self.sr.run_once()
        reservations = FileDataStore(self.test_file).read()
        seat = reservations[0][0]
        self.assertFalse(seat.reserved)

    def test_view(self):
        self.sr.view()

    def test_get_location(self):
        expected_row = 2
        expected_col = 2
        row, col = self.sr.get_location('C2')
        self.assertEqual(row, expected_row)
        self.assertEqual(col, expected_col)

    def test_get_letter(self):
        expected_letter = 'E'
        self.assertEqual(self.sr.get_letter('E2'), expected_letter)

    def test_is_reserved(self):
        self.sr.process_action('Book E2 1')
        reservations = FileDataStore(self.test_file).read()
        seat_location = 'E2'
        self.assertTrue(self.sr.is_reserved(reservations, seat_location))

    def test_is_reservable(self):
        self.sr.start_seat = 'D0'
        self.sr.num_consecutive_seats = 3
        reservations = FileDataStore(self.test_file).read()
        self.assertTrue(self.sr.is_reservable(reservations))

    def test_is_not_reservable(self):
        self.sr.process_action('Book b0 3')
        self.sr.start_seat = 'B0'
        self.sr.num_consecutive_seats = 1
        reservations = FileDataStore(self.test_file).read()
        self.assertFalse(self.sr.is_reservable(reservations))

    def test_is_unreservable(self):
        self.sr.process_action('Book b0 3')
        self.sr.start_seat = 'B0'
        self.sr.num_consecutive_seats = 3
        reservations = FileDataStore(self.test_file).read()
        self.assertTrue(self.sr.is_unreservable(reservations))

    def test_is_not_unreservable(self):
        self.sr.start_seat = 'D0'
        self.sr.num_consecutive_seats = 1
        reservations = FileDataStore(self.test_file).read()
        self.assertFalse(self.sr.is_unreservable(reservations))

    def test_book(self):
        self.sr.start_seat = 'D0'
        self.sr.num_consecutive_seats = 1
        self.sr.book()

    def test_reserve_seat(self):
        self.sr.start_seat = 'A2'
        self.sr.num_consecutive_seats = 1
        reservations = FileDataStore(self.test_file).read()
        self.sr.reserve_seat(reservations)

    def test_unreserve_seat(self):
        self.sr.start_seat = 'A0'
        self.sr.num_consecutive_seats = 1
        reservations = FileDataStore(self.test_file).read()
        self.sr.unreserve_seat(reservations)

    def test_cancel(self):
        self.sr.start_seat = 'D0'
        self.sr.num_consecutive_seats = 1
        self.sr.cancel()
