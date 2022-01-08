import pickle


class FileDataStore(object):
    def __init__(self, filename, reservations=None):
        self.fn = filename
        self.res = reservations

    def write(self):
        """
        Store initialized 2D array object in a file
        :return:
        """
        try:
            with open(self.fn, 'wb') as f:
                pickle.dump(self.res, f)
        except FileNotFoundError:
            return

    def read(self):
        """
        Restore 2D array object from a file
        :return: 2D array object
        """
        try:
            with open(self.fn, 'rb') as f:
                obj = pickle.load(f)
                return obj
        except FileNotFoundError:
            return

    def update(self, reservations):
        """
        Update file with new reservations
        :param reservations:
        :return:
        """
        try:
            with open(self.fn, 'wb') as f:
                pickle.dump(reservations, f)
        except FileNotFoundError:
            return
