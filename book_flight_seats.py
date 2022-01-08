from reservation import SeatReservation

if __name__ == '__main__':
    sr = SeatReservation('reservations.txt', 20, 8)
    sr.process_request2()
