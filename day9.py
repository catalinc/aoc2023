#!/usr/bin/env python3

import regex as re
from utils import get_day_input


def parse_history(s: str) -> list[int]:
    return [int(x) for x in re.split(r"\s+", s)]


def all_equal(history: list[int]) -> bool:
    for i in range(1, len(history)):
        if history[i] != history[i - 1]:
            return False
    return True


def predict_forward(history: list[int]) -> int:
    ans = history[-1]
    while not all_equal(history):
        new_history = []
        for i in range(1, len(history)):
            new_history.append(history[i] - history[i - 1])
        history = new_history
        ans += history[-1]
    return ans


def predict_backward(history: list[int]) -> int:
    buf = [history[0]]
    while not all_equal(history):
        new_history = []
        for i in range(1, len(history)):
            new_history.append(history[i] - history[i - 1])
        history = new_history
        buf.append(history[0])
    while len(buf) > 1:
        right = buf.pop()
        left = buf.pop()
        buf.append(left - right)
    return buf[0]


def part1(histories: list[list[int]]):
    return sum(predict_forward(h) for h in histories)


def part2(histories: list[list[int]]):
    return sum(predict_backward(h) for h in histories)


def main():
    lines = get_day_input(9)
    histories = [parse_history(line) for line in lines]
    print(part1(histories))
    print(part2(histories))


if __name__ == "__main__":
    main()
