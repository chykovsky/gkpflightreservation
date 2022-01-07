import pickle
from copy import deepcopy


class FileDataStore(object):
    def __init__(self, filename, reservations):
        self.fn = filename
        self.res = reservations
        self.res_original = deepcopy(reservations)

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

    def update(self, reservations):
        try:
            with open(self.fn, 'wb') as f:
                pickle.dump(reservations, f)
        except FileNotFoundError:
            return

    def reset(self):
        self.res = self.res_original
        self.update(self.res_original)
