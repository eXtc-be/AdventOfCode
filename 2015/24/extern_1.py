#!/usr/bin/python

"""
Module-specific doc string.
"""

import itertools
from functools import reduce


def product(x):
    return reduce(lambda z, y: z * y, x, 1)


def main():
    with open('./input_2015_24', "r") as f:
        lines = f.readlines()

    packages = []
    for line in lines:
        packages.append(int(line))

    total = sum(packages)
    target = total // 3
    print(f'{total = }; {target = }')

    combos = []
    for l in range(1, len(packages)):
        combos = []
        for n in itertools.combinations(packages, l):
            if sum(n) == target:
                combos.append(n)

        print(f'{l = }; combos = {len(combos)}')
        if combos:
            break

    c = min(combos, key=product)
    print(c)
    print(product(c))


if __name__ == "__main__":
    main()

# vim: set et sw=4 ts=4:
