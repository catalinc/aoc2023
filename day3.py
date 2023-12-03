#!/usr/bin/env python3

import regex as re
from utils import get_day_input
from typing import NamedTuple
from collections import defaultdict

directions = [(-1, -1),
              (-1, 0),
              (-1, 1),
              (0, -1),
              (0, 1),
              (1, -1),
              (1, 0),
              (1, 1)]


class Number(NamedTuple):
    value: int
    line: int
    start: int
    end: int


def parse_numbers(schematic: list[str]) -> list[Number]:
    numbers = []
    for i, line in enumerate(schematic):
        for m in re.finditer(r"\d+", line):
            value = int(m.group())
            start, end = m.span()
            numbers.append(Number(value=value, line=i, start=start, end=end))
    return numbers


def is_part_number(number: Number, schematic: list[str]) -> bool:
    num_lines, num_cols = len(schematic), len(schematic[0])
    for column in range(number.start, number.end):
        for d in directions:
            n_lin = number.line + d[0]
            n_col = column + d[1]
            if n_lin < 0 or n_lin >= num_lines or n_col < 0 or n_col >= num_cols:
                continue
            c = schematic[n_lin][n_col]
            if c.isdigit() or c == ".":
                continue
            return True
    return False


class Gear(NamedTuple):
    line: int
    column: int


def get_adjacent_gears(number: Number, schematic: list[str]) -> set[Gear]:
    gears: set[Gear] = set()
    for column in range(number.start, number.end):
        num_lines, num_cols = len(schematic), len(schematic[0])
        for d in directions:
            n_lin = number.line + d[0]
            n_col = column + d[1]
            if n_lin < 0 or n_lin >= num_lines or n_col < 0 or n_col >= num_cols:
                continue
            c = schematic[n_lin][n_col]
            if c == "*":
                gears.add(Gear(line=n_lin, column=n_col))
    return gears


def part1(schematic: list[str]):
    numbers = parse_numbers(schematic)
    return sum(number.value for number in numbers if is_part_number(number, schematic))


def part2(schematic: list[str]):
    numbers = parse_numbers(schematic)
    part_numbers = [number for number in numbers if is_part_number(number, schematic)]
    gears_map: dict[Gear, list[Number]] = defaultdict(list)
    for pn in part_numbers:
        gears = get_adjacent_gears(pn, schematic)
        for g in gears:
            gears_map[g].append(pn)
    total_ratio = 0
    for _, pns in gears_map.items():
        if len(pns) == 2:
            total_ratio += pns[0].value * pns[1].value
    return total_ratio


def main():
    schematic = get_day_input(3)
    print(part1(schematic))
    print(part2(schematic))


if __name__ == "__main__":
    main()
