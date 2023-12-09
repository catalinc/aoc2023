#!/usr/bin/env python3
from dataclasses import dataclass
from math import lcm

import regex as re

from utils import get_day_input_full_content


@dataclass
class DesertMap:
    instructions: str
    network: dict[str, dict[str, str]]


def parse_input(s: str) -> DesertMap:
    lines = [line for line in s.split("\n") if line]
    instructions = lines[0]
    network = {}
    for line in lines[1:]:
        node, left, right, = re.findall(r"\w{3}", line)
        network[node] = {"L": left, "R": right}
    return DesertMap(instructions=instructions, network=network)


def part1(dm: DesertMap, start: str = "AAA", end: str = "ZZZ") -> int:
    node, i, steps = start, 0, 0
    while node != end:
        node = dm.network[node][dm.instructions[i]]
        i = (i + 1) % len(dm.instructions)
        steps += 1
    return steps


def part2(dm: DesertMap) -> int:
    start_nodes = [node for node in dm.network.keys() if node[-1] == "A"]
    periods = {}
    for node in start_nodes:
        periods[node] = find_period(node, dm)
    return lcm(*(v for v in periods.values()))


def find_period(start: str, dm: DesertMap, max_steps: int = 100_000) -> int:
    node, i, steps = start, 0, 0
    ends = []
    while steps < max_steps:
        node = dm.network[node][dm.instructions[i]]
        i = (i + 1) % len(dm.instructions)
        steps += 1
        if node[-1] == "Z":
            ends.append(steps)
        if len(ends) == 2:
            return ends[1] - ends[0]


def main():
    s = get_day_input_full_content(8)
    dm = parse_input(s)
    print(part1(dm))
    print(part2(dm))


if __name__ == "__main__":
    main()
