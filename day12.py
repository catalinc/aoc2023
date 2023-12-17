#!/usr/bin/env python3
from dataclasses import dataclass
from functools import cache

from utils import get_day_input_full_content, parse_ints


@dataclass
class Record:
    conditions: str
    rules: tuple[int, ...]

    def unfold(self) -> "Record":
        conditions = "?".join(self.conditions for _ in range(5))
        rules = self.rules * 5
        return Record(conditions=conditions, rules=rules)


def parse_records(s: str) -> list[Record]:
    records = []
    for line in s.split("\n"):
        if not line:
            continue
        parts = line.split(" ")
        conditions, rules = parts[0], tuple(parse_ints(parts[1]))
        records.append(Record(conditions=conditions, rules=rules))
    return records


@cache
def arrangements(conditions, rules):
    if not rules:
        return 0 if "#" in conditions else 1
    if not conditions:
        return 1 if not rules else 0

    result = 0

    if conditions[0] in ".?":
        result += arrangements(conditions[1:], rules)
    if conditions[0] in "#?":
        if rules[0] <= len(conditions) and "." not in conditions[: rules[0]] and (
                rules[0] == len(conditions) or conditions[rules[0]] != "#"):
            result += arrangements(conditions[rules[0] + 1:], rules[1:])
    return result


def part1(records: list[Record]):
    return sum(arrangements(r.conditions, r.rules) for r in records)


def part2(records: list[Record]):
    records = [r.unfold() for r in records]
    return part1(records)


def main():
    s = get_day_input_full_content(12)
    records = parse_records(s)
    print(part1(records))
    print(part2(records))


if __name__ == "__main__":
    main()
