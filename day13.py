#!/usr/bin/env python3
from collections import namedtuple
from utils import get_day_input_full_content

Pattern = namedtuple("Pattern", ["rows", "cols"])


def parse_patterns(s: str) -> list[Pattern]:
    patterns = []
    for block in s.split("\n\n"):
        rows = [r for r in block.split("\n") if r]
        cols = []
        for i in range(len(rows[0])):
            col = ""
            for j in range(len(rows)):
                col += rows[j][i]
            cols.append(col)
        patterns.append(Pattern(rows=rows, cols=cols))
    return patterns


def find_reflection(pattern: Pattern) -> tuple[str, int]:
    for i in range(len(pattern.cols) - 1):
        j, k = i, i + 1
        while j >= 0 and k < len(pattern.cols) and pattern.cols[j] == pattern.cols[k]:
            j -= 1
            k += 1
        if j < 0 or k >= len(pattern.cols):
            return "v", i + 1
    for i in range(len(pattern.rows) - 1):
        j, k = i, i + 1
        while j >= 0 and k < len(pattern.rows) and pattern.rows[j] == pattern.rows[k]:
            j -= 1
            k += 1
        if j < 0 or k >= len(pattern.rows):
            return "h", i + 1
    return "", -1


scoring = {
    "v": lambda x: x,
    "h": lambda x: x * 100,
}


def part1(patterns: list[Pattern]) -> int:
    return sum(scoring[o](n) for o, n in (find_reflection(p) for p in patterns))


def part2(patterns: list[Pattern]) -> int:
    pass


def main():
    s = get_day_input_full_content(13)
    patterns = parse_patterns(s)
    print(part1(patterns))
    print(part2(patterns))


if __name__ == "__main__":
    main()
