from datastore import FileDataStore
from seat import Seat
import re


BOOK_CANCEL_INFO = """
\tExpected format [Action] [Starting Seat] [Number of consecutive seats needed]
\tAction: BOOK or CANCEL
\tStarting Seat: A0 - T7
\tNumber of consecutive seats needed: 1 - 8
"""

row_letter_index_map = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    'I': 8,
    'J': 9,
    'K': 10,
    'L': 11,
    'M': 12,
    'N': 13,
    'O': 14,
    'P': 15,
    'Q': 16,
    'R': 17,
    'S': 18,
    'T': 19
}


class SeatReservation(object):
    def __init__(self, filename, rows, cols):
        self.rows, self.seats_per_row = (rows, cols)
        self.reservations = [[Seat() for _ in range(self.seats_per_row)] for _ in range(self.rows)]
        self.fds = FileDataStore(filename, self.reservations)
        self.fds.write()
        self.action = None
        self.start_seat = None
        self.num_consecutive_seats = None

    def process_request(self):
        booking_details = input('Book or Cancel a seat reservation: ')
        regex = re.compile('\s*(book|cancel)\s+[a-t][0-7]\s+[1-8]\s*', re.IGNORECASE)
        m = regex.match(booking_details)

        if m:
            self.action, self.start_seat, self.num_consecutive_seats = m.group().split()
            self.num_consecutive_seats = int(self.num_consecutive_seats)

            if self.action.upper() == 'BOOK':
                print(self.book())

            if self.action.upper() == 'CANCEL':
                print(self.cancel())
        else:
            print('%s%s' % ('Invalid Input entered: ', BOOK_CANCEL_INFO))
            exit(1)

    @classmethod
    def get_location(cls, ss):
        """
        Return row number corresponding to row letter received
        :param ss: starting seat e.g A0, B1, T7
        :return:
        """
        a = [i for i in ss]

        return int(row_letter_index_map[a[0].upper()]), int(a[1])

    @classmethod
    def get_letter(cls, seat_location):
        for i in seat_location:
            return i.upper()

    def is_reserved(self, reservation, seat_location):
        """
        Check if seat is reserved
        :param reservation:
        :param seat_location:
        :return:
        """
        row, col = self.get_location(seat_location)
        seat = reservation[row][col]

        if not seat.reserved:
            return False

        return True

    def is_reservable(self, reservations):
        """

        :param reservations:
        :return: True or False
        """
        if self.is_reserved(reservations, self.start_seat):
            return False

        row, col = self.get_location(self.start_seat)
        row_letter = self.get_letter(self.start_seat)
        max_index = col + (self.num_consecutive_seats - 1)

        if max_index > len(reservations[row]) - 1:
            return False

        for seat_index in range(col + 1, (col + 1 + self.num_consecutive_seats)):
            if self.is_reserved(reservations, '{}{}'.format(row_letter, seat_index)):
                return False

        return True

    def is_unreservable(self, reservation):
        row, col = self.get_location(self.start_seat)
        row_letter = self.get_letter(self.start_seat)
        max_index = col + (self.num_consecutive_seats - 1)

        if max_index > len(reservation[row]) - 1:
            return False

        for seat_index in range(col, (col + self.num_consecutive_seats + 1)):
            if not self.is_reserved(reservation, '{}{}'.format(row_letter, seat_index)):
                return False

        return True

    def book(self):
        """

        :return:
        """
        reservations = self.fds.read()
        if not reservations:
            return 'Fail'

        if self.is_reservable(reservations):
            self.reserve_seat(reservations)
            self.fds.update(reservations)
            return 'Success'

        return 'Fail'

    def reserve_seat(self, reservation):
        row, col = self.get_location(self.start_seat)

        for seat_column in range(col, col + self.num_consecutive_seats + 1):
            seat = reservation[row][seat_column]
            seat.reserve()

    def unreserve_seat(self, reservation):
        row, col = self.get_location(self.start_seat)

        for seat_column in range(col, col + self.num_consecutive_seats + 1):
            seat = reservation[row][seat_column]
            seat.unreserve()

    def cancel(self):
        """

        :return:
        """
        reservations = self.fds.read()
        if not reservations:
            return 'Fail'

        if self.is_unreservable(reservations):
            self.unreserve_seat(reservations)
            self.fds.update(reservations)
            return 'Success'

        return 'Fail'

    def reset(self):
        self.fds.reset()
