from reservation import SeatReservation

MSG = """
Welcome to GKP airlines!
Type quit to exit at any time.
Do you want to run our app as a service? yes or no: 
"""

if __name__ == '__main__':
    sr = SeatReservation('reservations.txt', 20, 8)
    while True:
        run_type = input(MSG)
        if run_type.upper().strip() == 'YES':
            sr.service()
            break
        elif run_type.upper().strip() == 'NO':
            sr.run_once()
            break
        else:
            continue
