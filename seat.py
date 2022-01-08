class Seat(object):
    def __init__(self, row, col):
        self.reserved = False
        self.row = row
        self.col = col

    def reserve(self):
        self.reserved = True

    def unreserve(self):
        self.reserved = False

    def __str__(self):
        if self.reserved:
            state = 'booked'
        else:
            state = 'open'
        # return 'Seat {}'.format(state)
        return 'Seat{}{} {}'.format(self.row, self.col, state)

    def __repr__(self):
        if self.reserved:
            state = 'booked'
        else:
            state = 'open'
        return 'Seat{}{} {}'.format(self.row, self.col, state)
