#!/usr/bin/env python3
import sys
from dataclasses import dataclass, field
import regex as re

from utils import get_day_input_full_content, chunks


@dataclass
class RangeMap:
    start: int
    end: int
    base: int

    def get(self, key: int) -> int | None:
        if key < self.start:
            return None
        if key >= self.end:
            return None
        return self.base + (key - self.start)


@dataclass
class CategoryMap:
    name: str
    ranges: list[RangeMap] = field(default_factory=list)

    def get(self, key: int) -> int:
        first = self.ranges[0]
        last = self.ranges[-1]
        if key >= last.end:
            return False
        if key < first.start:
            return False
        lo, hi = 0, len(self.ranges) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            r = self.ranges[mid]
            if r.start <= key < r.end:
                return r.get(key)
            if r.start > key:
                hi = mid - 1
            if r.end <= key:
                lo = mid + 1
        return key

    def __post_init__(self):
        self.ranges.sort(key=lambda r: r.start)


class Almanac:
    _path = [
        'seed-to-soil',
        'soil-to-fertilizer',
        'fertilizer-to-water',
        'water-to-light',
        'light-to-temperature',
        'temperature-to-humidity',
        'humidity-to-location']

    def __init__(self, seeds: list[int], maps: dict[str, CategoryMap]) -> None:
        self.seeds = seeds
        self.maps = maps

    def get_location(self, key: int) -> int | None:
        for name in self._path:
            key = self.maps[name].get(key)
        return key


def parse_seeds(s: str) -> list[int]:
    return [int(x.group()) for x in re.finditer(r"\d+", s)]


def parse_range_map(s: str) -> RangeMap:
    base, start, size = [int(x) for x in s.split(" ")]
    return RangeMap(start=start, end=start + size, base=base)


def parse_category_map(s: str) -> CategoryMap:
    lines = s.split("\n")
    name = lines[0].split(" ")[0]
    ranges = [parse_range_map(line) for line in lines[1:] if line]
    return CategoryMap(name=name, ranges=ranges)


def parse_almanac(s: str) -> Almanac:
    sections = s.split("\n\n")
    seeds = parse_seeds(sections[0])
    maps = {c.name: c for c in (parse_category_map(section) for section in sections[1:])}
    return Almanac(seeds=seeds, maps=maps)


def part1(almanac: Almanac) -> int:
    return min(almanac.get_location(seed) for seed in almanac.seeds)


def part2(almanac: Almanac) -> int:
    # Brute-force, run with pypy3, takes about 1h to finish
    seed_ranges = [(lst[0], lst[0] + lst[1]) for lst in chunks(almanac.seeds, 2)]
    lowest = sys.maxsize
    for sr in seed_ranges:
        for seed in range(sr[0], sr[1]):
            lowest = min(lowest, almanac.get_location(seed))
    return lowest


def main():
    s = get_day_input_full_content(5)
    almanac = parse_almanac(s)
    print(part1(almanac))
    print(part2(almanac))


if __name__ == "__main__":
    main()
