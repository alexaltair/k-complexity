# --- I ran this for a long time and it never output anything. So maybe I messed up the implementation.


# A hopefully universal Turing machine from Table 6.2.14 of
# https://www.ini.uzh.ch/~tneary/tneary_Thesis.pdf
from collections import deque
import sys

# The state transition table
#   |   u1 |   u2 |   u3 |   u4 |   u5 |   u6 |   u7 |   u8 |    u9 |   u10 |   u11 |   u12 |   u13 |   u14 |   u15
# c | cRu2 | bRu3 | cLu7 | cLu6 | bRu1 | bLu4 | cLu8 | bLu9 |  cRu1 | bLu11 | cRu12 | cRu13 |  cLu2 |  cLu3 | cRu14
# b | bRu1 | bRu1 | cLu5 | bLu5 | bLu4 | bLu4 | bLu7 | bLu7 | bLu10 |  HALT | bRu14 | bRu12 | bRu12 | cRu15 | bRu14
# c is the blank character, so the tape is infinite in both directions and has c written everywhere by default.

state_transitions = {
    0: [
        (0, 1, 1),
        (1, 1, 2),
        (0, -1, 6),
        (0, -1, 5),
        (1, 1, 0),
        (1, -1, 3),
        (0, -1, 7),
        (1, -1, 8),
        (0, 1, 0),
        (1, -1, 10),
        (0, 1, 11),
        (0, 1, 12),
        (0, -1, 1),
        (0, -1, 2),
        (0, 1, 13),
    ],
    1: [
        (1, 1, 0),
        (1, 1, 0),
        (0, -1, 4),
        (1, -1, 4),
        (1, -1, 3),
        (1, -1, 3),
        (1, -1, 6),
        (1, -1, 6),
        (1, -1, 9),
        'HALT',
        (1, 1, 13),
        (1, 1, 11),
        (1, 1, 11),
        (0, 1, 14),
        (1, 1, 13),
    ],
}


initial_tape = ''
if len(sys.argv) > 1:
    initial_tape = sys.argv[1]

# The tape is a deque so we can efficiently append and pop to both sides
tape = deque(initial_tape)
head = len(initial_tape)
current_state = 0

def tape_bit_at_index(index):
    if (index < 0) or (index >= len(tape)) or not tape[index]:
        return 0
    return 1

def write_to_tape(head, bit):
    if head == -1:
        tape.appendleft(bit)
        head = 0
    elif 0 <= head < len(tape):
        tape[head] = bit
    elif head == len(tape):
        tape.append(bit)
    else:
        raise ValueError(f"Invalid head index: {index}")

    return head

def print_tape():
    for bit in tape:
        print(bit, end='')
    print('')


while True:
    print_tape()
    rule = state_transitions[tape_bit_at_index(head)][current_state]
    if rule == 'HALT':
        print('HALT')
        break

    head = write_to_tape(head, rule[0])
    head += rule[1]

    current_state = rule[2]


print_tape()
