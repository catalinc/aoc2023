#!/usr/bin/env python3


import regex as re
from utils import get_day_input_full_content
from dataclasses import dataclass


@dataclass
class Race:
    time: int
    distance: int


def parse_races(s: str) -> list[Race]:
    times, distances = s.split("\n")[0:2]
    times = [int(m.group()) for m in re.finditer(r"\d+", times)]
    distances = [int(m.group()) for m in re.finditer(r"\d+", distances)]
    return [Race(time=t, distance=d) for t, d in zip(times, distances)]


def count_ways_to_win(r: Race) -> int:
    ways = 0
    for t in range(0, r.time + 1):
        d = t * (r.time - t)
        if d > r.distance:
            ways += 1
    return ways


def parse_one_race(s: str) -> Race:
    time, distance = s.split("\n")[0:2]
    time = int("".join(m.group() for m in re.finditer(r"\d+", time)))
    distance = int("".join(m.group() for m in re.finditer(r"\d+", distance)))
    return Race(time=time, distance=distance)


def part1(races: list[Race]) -> int:
    p = 1
    for r in races:
        p *= count_ways_to_win(r)
    return p


def part2(race: Race) -> int:
    return count_ways_to_win(race)


def main():
    s = get_day_input_full_content(6)
    races = parse_races(s)
    race = parse_one_race(s)
    print(part1(races))
    print(part2(race))


if __name__ == "__main__":
    main()
