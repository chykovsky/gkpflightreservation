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


row_letter_index_map = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    'I': 8,
    'J': 9,
    'K': 10,
    'L': 11,
    'M': 12,
    'N': 13,
    'O': 14,
    'P': 15,
    'Q': 16,
    'R': 17,
    'S': 18,
    'T': 19
}
