# 20 rows i.e. 0 - 19 or A to T
# 8 seats per row i.e. 0 - 7
# Input: [Action] [Starting Seat] [Number of consecutive seats]
# Action = BOOK or CANCEL
#   Add functionality to use lowercase book or cancel
#   Reject everything else
#   If case insensitive, apply that to row letter as well i.e. A0 = a0 and B0  = b0
#   If not case insensitive, A0 != a0
# Only letters A - T are allowed. If case insensitive, also allow a - t
# Numbers indicating sit in a row can only be in [0 .. 7]
# Cancelling an unoccupied seat should result in a Fail
# Add functionality if more messages would like to be seen concerning what issue happened.
#   Maybe use a global flag or do that. So it prints "Fail" and adds a context to it.
# Output: Success or Fail
import re
import pickle

BOOK_CANCEL_INFO = """
\tExpected format [Action] [Starting Seat] [Number of consecutive seats needed]
\tAction: BOOK or CANCEL
\tStarting Seat: A0 - T7
\tNumber of consecutive seats needed: 1 - 8
"""

booking_details = input('Book or Cancel a seat reservation: ')
regex = re.compile('\s*(book|cancel)\s+[a-t][0-7]\s+[1-8]\s*', re.IGNORECASE)
m = regex.match(booking_details)

action, start_seat, num_consecutive_seats = "", "", 0
if m:
    action, start_seat, num_consecutive_seats = m.group().split()
else:
    print('%s%s' % ('Invalid Input entered: ', BOOK_CANCEL_INFO))
    exit(1)

print(action, start_seat, num_consecutive_seats)
