class Seat(object):
    def __init__(self):
        self.reserved = False

    def reserve(self):
        self.reserved = True

    def unreserve(self):
        self.reserved = False

    def __str__(self):
        pass
