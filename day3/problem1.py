#!/usr/bin/env python3

"""
--- Day 3: Crossed Wires ---

The gravity assist was successful, and you're well on your way to the Venus
refuelling station. During the rush back on Earth, the fuel management system
wasn't completely installed, so that's next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires are
connected to a central port and extend outward on a grid. You trace the path
each wire takes as it leaves the central port, one wire per line of text (your
puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix the
circuit, you need to find the intersection point closest to the central port.
Because the wires are on a grid, use the Manhattan distance for this
measurement. While the wires do technically cross right at the central port
where they both start, this point does not count, nor does a wire count as
crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the
central port (o), it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........

Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4,
and left 4:

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

These wires cross at two locations (marked X), but the lower-left one is closer
to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135

What is the Manhattan distance from the central port to the closest
intersection?

"""

import operator
import os.path
import unittest
from functools import reduce


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
    intersections = find_all_intersections(paths)
    distances = map(convert_to_manhattan, intersections)
    return sorted(distances)[0]


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


STEPS = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1),
}


def convert_to_manhattan(point):
    x, y = point
    return abs(x) + abs(y)


class TestProblem(unittest.TestCase):

    def test_find_closer_intersection(self):

        cases = (
            ('R75,D30,R83,U83,L12,D49,R71,U7,L72',
             'U62,R66,U55,R34,D71,R55,D58,R83', 159),
            ('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
             'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7', 135),
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
