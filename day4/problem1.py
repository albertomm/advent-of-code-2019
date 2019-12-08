#!/usr/bin/env python3

"""
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected by a
password. The Elves had written the password on a sticky note, but someone threw
it out.

However, they do remember a few key facts about the password:

 * It is a six-digit number.
 * The value is within the range given in your puzzle input.
 * Two adjacent digits are the same (like 22 in 122345).
 * Going from left to right, the digits never decrease; they only ever increase
   or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

 * 111111 meets these criteria (double 11, never decreases).
 * 223450 does not meet these criteria (decreasing pair of digits 50).
 * 123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet
these criteria?
"""

import os.path
import string
import unittest


def solve():

    # Read the input
    input_dir = os.path.dirname(__file__)
    input_path = os.path.join(input_dir, 'input.txt')
    with open(input_path, 'r') as fd:
        input_params = fd.readline()

    # Parse the input parameters
    pw_min, _, pw_max = input_params.partition('-')
    pw_min = int(pw_min)
    pw_max = int(pw_max)
    print('Input:', pw_min, pw_max)

    # Generate and validate all the possible passwords
    possible_passwords = generate_passwords(pw_min, pw_max)
    valid_passwords = filter(validate_password, possible_passwords)

    #  Count the possible passwords
    result = sum(1 for _ in valid_passwords)
    print(result)


def generate_passwords(pw_min, pw_max):
    return (str(pw) for pw in range(pw_min, pw_max))


def validate_password(password):
    return is_rising(password) and has_double(password)


def is_rising(password):
    return sorted(password) == list(password)


def has_double(password):
    for d in DOUBLES:
        if d in password:
            return True
    return False


DOUBLES = tuple(2 * digit for digit in string.digits)


class TestProblem(unittest.TestCase):

    def test_validate_password(self):

        cases = (
            ('111111', True),
            ('223450', False),
            ('123789', False),
        )

        for case, expected in cases:
            result = validate_password(case)
            self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
    print()
    solve()
