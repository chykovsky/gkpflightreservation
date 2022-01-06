import pickle


class FileDataStore(object):
    def __init__(self, filename, reservations):
        self.fn = filename
        self.res = reservations

    def write(self):
        try:
            with open(self.fn, 'wb') as f:
                pickle.dump(self.res, f)
        except FileNotFoundError:
            return

    def read(self):
        try:
            with open(self.fn, 'rb') as f:
                obj = pickle.load(f)
                return obj
        except FileNotFoundError:
            return
