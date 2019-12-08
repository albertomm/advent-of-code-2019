#!/usr/bin/env python3

"""
--- Part Two ---

An Elf just remembered one more important detail: the two adjacent matching
digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the
following are now true:

 * 112233 meets these criteria because the digits never decrease and all
   repeated digits are exactly two digits long.
 * 123444 no longer meets the criteria (the repeated 44 is part of a larger
   group of 444).
 * 111122 meets the criteria (even though 1 is repeated more than twice, it
   still contains a double 22).

How many different passwords within the range given in your puzzle input meet
all of the criteria?
"""

import os.path
import string
import unittest
import re


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

    current = ''
    repetitions = 0

    for char in password:
        if char != current:
            current = char
            if repetitions == 2:
                break
            repetitions = 1
        else:
            repetitions += 1

    return repetitions == 2


class TestProblem(unittest.TestCase):

    def test_validate_password(self):

        cases = (
            ('112233', True),
            ('123444', False),
            ('111122', True),
        )

        for case, expected in cases:
            result = validate_password(case)
            self.assertEqual(result, expected, case)


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
    print()
    solve()
