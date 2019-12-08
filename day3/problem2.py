#!/usr/bin/env python3

"""
--- Part Two ---

It turns out that this circuit is very timing-sensitive; you actually need to
minimize the signal delay.

To do this, calculate the number of steps each wire takes to reach each
intersection; choose the intersection where the sum of both wires' steps is
lowest. If a wire visits a position on the grid multiple times, use the steps
value from the first time it visits that position when calculating the total
value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire
has entered to get to that location, including the intersection being
considered. Again consider the example from above:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

In the above example, the intersection closest to the central port is reached
after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second
wire for a total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2 =
15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

 * R75,D30,R83,U83,L12,D49,R71,U7,L72
   U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
 * R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
   U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps

What is the fewest combined steps the wires must take to reach an intersection?

"""

import operator
import os.path
import unittest
from functools import reduce
from operator import itemgetter


def solve():

    # Read the input
    input_dir = os.path.dirname(__file__)
    input_path = os.path.join(input_dir, 'input.txt')
    with open(input_path, 'r') as fd:
        wire_strings = fd.readlines()

    # Parse the input lines into wire steps
    wires = (
        line.split(',')
        for line in wire_strings
    )

    # Calculate the closer intersection
    result = find_closer_intersection(wires)
    print(result)


def find_closer_intersection(wires):
    paths = map(calculate_path, wires)
    paths = tuple(map(tuple, paths))
    intersections = find_all_intersections(paths)
    return get_first_intersection_timing(intersections, paths)


def calculate_path(movements):
    current = (0, 0)
    for movement in movements:
        direction = movement[0]
        distance = int(movement[1:])
        for current in walk(current, direction, distance):
            yield current


def walk(current, direction, distance):
    current_x, current_y = current
    delta_x, delta_y = STEPS[direction]
    for _ in range(distance):
        current_x += delta_x
        current_y += delta_y
        yield (current_x, current_y)


def find_all_intersections(paths):
    paths = map(set, paths)
    return reduce(operator.and_, paths)


def get_first_intersection_timing(intersections, paths):

    result = sum(map(len, paths))

    for intersection in intersections:
        timing = sum(
            path.index(intersection) + 1
            for path in paths
        )
        result = min(result, timing)

    return result


STEPS = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1),
}


class TestProblem(unittest.TestCase):

    def test_find_closer_intersection(self):

        cases = (
            ('R75,D30,R83,U83,L12,D49,R71,U7,L72',
             'U62,R66,U55,R34,D71,R55,D58,R83', 610),
            ('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
             'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7', 410),
        )

        for wire1, wire2, expected in cases:
            wire1 = wire1.split(',')
            wire2 = wire2.split(',')
            result = find_closer_intersection((wire1, wire2))
            self.assertEqual(result, expected)

    def test_calculate_path(self):

        movements = ('R2', 'U3', 'L4', 'D1')
        result = tuple(calculate_path(movements))
        expected = (
            (1, 0), (2, 0),
            (2, 1), (2, 2), (2, 3),
            (1, 3), (0, 3), (-1, 3), (-2, 3),
            (-2, 2),
        )
        self.assertSequenceEqual(result, expected)

    def test_walk(self):

        cases = (
            ((1, 1), 'R', 4, ((2, 1), (3, 1), (4, 1), (5, 1))),
            ((2, 3), 'L', 3, ((1, 3), (0, 3), (-1, 3))),
            ((5, 7), 'U', 5, ((5, 8), (5, 9), (5, 10), (5, 11), (5, 12))),
            ((4, 1), 'D', 3, ((4, 0), (4, -1), (4, -2))),
        )

        for current, direction, distance, expected in cases:
            result = walk(current, direction, distance)
            self.assertSequenceEqual(tuple(result), expected)


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
    print()
    solve()
