#!/usr/bin/env python3

import regex as re
from utils import get_day_input
from dataclasses import dataclass, field


@dataclass
class Card:
    num: int
    win: list[int] = field(default_factory=list)
    actual: list[int] = field(default_factory=list)


def parse_card(s: str) -> Card:
    h, t = s.split(":")
    num = int(re.findall(r"\d+", s)[0])
    s1, s2 = t.split("|")
    win = [int(x.group()) for x in re.finditer(r"\d+", s1)]
    actual = [int(x.group()) for x in re.finditer(r"\d+", s2)]
    return Card(num=num, win=win, actual=actual)


def score_card(card: Card) -> int:
    m = 0
    for n in card.win:
        if n in card.actual:
            m += 1
    return 0 if m == 0 else 2 ** (m - 1)


def count_wins(card: Card) -> int:
    m = 0
    for n in card.win:
        if n in card.actual:
            m += 1
    return m


def part1(cards: list[Card]):
    return sum(score_card(c) for c in cards)


def part2(cards: list[Card]):
    wins = {c.num: count_wins(c) for c in cards}
    total = 0
    to_process = [c.num for c in cards]
    while to_process:
        new_cards = []
        for n in to_process:
            total += 1
            for i in range(n + 1, n + wins[n] + 1):
                new_cards.append(i)
        to_process = new_cards
    return total


def main():
    lines = get_day_input(4)
    cards = [parse_card(l) for l in lines]
    print(part1(cards))
    print(part2(cards))


if __name__ == "__main__":
    main()
