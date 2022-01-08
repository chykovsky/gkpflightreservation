from datastore import FileDataStore
from seat import Seat
import re
import os.path
import logging.config

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

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
        self.filename, self.rows, self.seats_per_row, = filename, rows, cols
        if not os.path.exists(self.filename):
            reservations = [[Seat(self.get_key_from_value(row), col) for col in range(self.seats_per_row)] for row in
                            range(self.rows)]
            self.fds = FileDataStore(self.filename, reservations)
            self.fds.write()
        self.action = None
        self.start_seat = None
        self.num_consecutive_seats = None

    def service(self):
        """
        Run as a service until you quit
        :return:
        """
        while True:
            booking_details = input('Book or Cancel a seat reservation: ')
            logger.debug('service booking_details: %s', booking_details)

            if 'quit'.upper() in booking_details.upper():
                exit(0)

            if 'view'.upper() in booking_details.upper():
                self.view()
                continue

            self.process_action(booking_details)

    def process_action(self, booking_details):
        regex = re.compile('\s*(book|cancel)\s+[a-t][0-7]\s+[1-8]\s*', re.IGNORECASE)
        m = regex.match(booking_details)
        if m:
            self.action, self.start_seat, self.num_consecutive_seats = m.group().split()
            self.num_consecutive_seats = int(self.num_consecutive_seats)
            logger.debug('action: %s, start_seat: %s, num_consecutive_seats: %s', self.action, self.start_seat,
                         self.num_consecutive_seats)

            if self.action.upper() == 'BOOK':
                result = self.book()
                logger.debug('result: %s', result)
                print(result)

            if self.action.upper() == 'CANCEL':
                result = self.cancel()
                logger.debug('result: %s', result)
                print(result)
        else:
            result = 'Fail'
            logger.debug('result: %s', result)
            print(result)

    def run_once(self):
        """
        Run once and exit
        :return:
        """
        print('Current seat map: ')
        self.view()
        booking_details = input('Book or Cancel a seat reservation: ')
        logger.debug('run_once booking_details: %s', booking_details)

        if 'quit'.upper() in booking_details.upper():
            exit(0)

        self.process_action(booking_details)

    def view(self):
        fds = FileDataStore(self.filename)
        print(fds.read())

    @classmethod
    def get_location(cls, seat_location):
        """
        Return row number corresponding to row letter received
        :param seat_location: seat location e.g A0, B1, T7
        :return: tuple of seat location integers
        """
        a = [i for i in seat_location]

        return int(row_letter_index_map[a[0].upper()]), int(a[1])

    @classmethod
    def get_letter(cls, seat_location):
        """
        Given a seat location e.g. A0, return the first character or row value e.g A
        :param seat_location: seat location
        :return: row value e.g A
        """
        for i in seat_location:
            return i.upper()

    def is_reserved(self, reservations, seat_location):
        """
        Check if seat is reserved
        :param reservations: 2D array of seat objects
        :param seat_location: seat location
        :return: True or False
        """
        row, col = self.get_location(seat_location)
        seat = reservations[row][col]

        if not seat.reserved:
            return False

        return True

    def is_reservable(self, reservations):
        """
        Validates whether a selection of seat(s) are reservable
        :param reservations: 2D array of seat objects
        :return: True or False
        """
        row, col = self.get_location(self.start_seat)
        row_letter = self.get_letter(self.start_seat)
        max_index = col + (self.num_consecutive_seats - 1)

        if max_index > len(reservations[row]) - 1:
            return False

        for seat_index in range(col, col + self.num_consecutive_seats):
            if self.is_reserved(reservations, '{}{}'.format(row_letter, seat_index)):
                return False

        return True

    def is_unreservable(self, reservations):
        """
        Validates whether a selection of seat(s) are unreservable
        :param reservations: 2D array of seat objects
        :return: True or False
        """
        row, col = self.get_location(self.start_seat)
        row_letter = self.get_letter(self.start_seat)
        max_index = col + (self.num_consecutive_seats - 1)

        if max_index > len(reservations[row]) - 1:
            return False

        for seat_index in range(col, col + self.num_consecutive_seats):
            if not self.is_reserved(reservations, '{}{}'.format(row_letter, seat_index)):
                return False

        return True

    def book(self):
        """
        Book a seat reservation
        :return: Success or Fail
        """
        fds = FileDataStore(self.filename)
        reservations = fds.read()
        logger.debug('{}: {}'.format('Reservations before booking', reservations))
        if not reservations:
            return 'Fail'

        if self.is_reservable(reservations):
            self.reserve_seat(reservations)
            fds.update(reservations)
            logger.debug('{}: {}'.format('Reservations after booking', reservations))
            return 'Success'

        return 'Fail'

    def reserve_seat(self, reservations):
        """
        Reserve a seat
        :param reservations: 2D array of seat objects
        :return:
        """
        row, col = self.get_location(self.start_seat)

        for seat_column in range(col, col + self.num_consecutive_seats):
            seat = reservations[row][seat_column]
            seat.reserve()

    def unreserve_seat(self, reservations):
        """
        Unreserves a booked seat.
        :param reservations: 2D array of seat objects
        :return:
        """
        row, col = self.get_location(self.start_seat)

        for seat_column in range(col, col + self.num_consecutive_seats):
            seat = reservations[row][seat_column]
            seat.unreserve()

    def cancel(self):
        """
        Cancel a seat reservation
        :return: Success or Fail
        """
        fds = FileDataStore(self.filename)
        reservations = fds.read()
        logger.debug('{}: {}'.format('Reservations before cancel', reservations))
        if not reservations:
            return 'Fail'

        if self.is_unreservable(reservations):
            self.unreserve_seat(reservations)
            fds.update(reservations)
            logger.debug('{}: {}'.format('Reservations after cancel', reservations))
            return 'Success'

        return 'Fail'

    @classmethod
    def get_key_from_value(cls, value):
        """
        Reverse a dictionary so values become keys and keys become values
        :param value: value
        :return: key
        """
        keys = list(row_letter_index_map.keys())
        values = list(row_letter_index_map.values())
        pos = values.index(value)

        return keys[pos]
