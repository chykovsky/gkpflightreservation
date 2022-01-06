from .datastore import FileDataStore

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
        self.reservations = [[0] * self.seats_per_row] * self.rows
        self.fds = FileDataStore(filename, self.reservations)

    @classmethod
    def get_starting_seat_indices(cls, ss):
        """
        Return row number corresponding to row letter received
        :param ss: starting seat e.g A0, B1, T7
        :return:
        """
        a = [i for i in ss]

        return int(row_letter_index_map[a[0]]), int(a[1])

    def is_reserved(self, reservation, seat):
        """
        Check if seat is reserved
        :param reservation:
        :param seat:
        :return:
        """
        row, col = self.get_starting_seat_indices(seat)
        if reservation[row][col] == 0:
            return False
        return True

    def is_reservable(self, reservation, ss, ncs):
        """

        :param reservation:
        :param ss: starting seat e.g A0, B1, T7
        :param ncs: number of consecutive seats to reserve e.g 1 or 3 or 5
        :return: True or False
        """
        if self.is_reserved(reservation, ss):
            return False

        row, col = self.get_starting_seat_indices(ss)
        max_index = col + (ncs - 1)

        if max_index > len(reservation[row]) - 1:
            return False

        for seat in range(col + 1, max_index + 1):
            if self.is_reserved(reservation, seat):
                return False

        return True

    def book(self, reservation, ss, ncs):
        """

        :param reservation:
        :param ss:
        :param ncs:
        :return:
        """
        if self.is_reservable(reservation, ss, ncs):
            pass

    def reserve_seat(self, reservation, ss, ncs):
        pass

    def cancel(self):
        """

        :return:
        """
        pass
