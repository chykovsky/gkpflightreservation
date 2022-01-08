class Seat(object):
    def __init__(self, row, col):
        self.reserved = False
        self.row = row
        self.col = col

    def reserve(self):
        """
        Reserve a seat
        :return:
        """
        self.reserved = True

    def unreserve(self):
        """
        Unreserve a seat
        :return:
        """
        self.reserved = False

    def __str__(self):
        """
        String representation of a seat object
        :return: string representation
        """
        if self.reserved:
            state = 'booked'
        else:
            state = 'open'
        return 'Seat{}{} {}'.format(self.row, self.col, state)

    def __repr__(self):
        """
        Repr representation of a seat object
        :return: repr representation
        """
        if self.reserved:
            state = 'booked'
        else:
            state = 'open'
        return 'Seat{}{} {}'.format(self.row, self.col, state)
