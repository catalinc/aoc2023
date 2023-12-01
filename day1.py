#!/usr/bin/env python3

import regex as re
from utils import get_day_input


def calibration_value(line: str) -> int:
    digits = re.findall(r"\d", line)
    first, last = int(digits[0]), int(digits[-1])
    return first * 10 + last


TR_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def to_int(s: str) -> int:
    n = TR_MAP.get(s)
    if n is not None:
        return n
    return int(s)


def calibration_value2(line: str) -> int:
    digits = re.findall(r"one|two|three|four|five|six|seven|eight|nine|\d", line, overlapped=True)
    first, last = to_int(digits[0]), to_int(digits[-1])
    return first * 10 + last


def part1(lines: list[str]) -> int:
    return sum(calibration_value(line) for line in lines)


def part2(lines: list[str]) -> int:
    return sum(calibration_value2(line) for line in lines)


def main():
    lines = get_day_input(1)
    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
