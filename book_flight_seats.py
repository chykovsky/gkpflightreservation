from reservation import SeatReservation

MSG = """
Welcome to GKP Airlines!
Type quit to exit at any time.
Do you want to run our app as a service? Enter yes or no: 
"""


def main():
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


if __name__ == '__main__':
    main()
