#!/usr/bin/env python3


from collections import Counter
from dataclasses import dataclass

from utils import get_day_input


@dataclass
class Hand:
    cards: str
    score: int
    ranks: tuple[int]
    best_score: int = 0  # with joker


def parse_hand(s: str, card_ranks: str = "23456789TJQKA") -> Hand:
    ranks = tuple([i for i in (card_ranks.index(c) for c in s)])
    common = Counter(s).most_common()
    if len(common) == 1:  # Five of a kind
        score = 6
    elif len(common) == 2:
        if common[0][1] == 4:  # Four of a kind
            score = 5
        else:  # Full house
            score = 4
    elif len(common) == 3:
        if common[0][1] == 3:
            score = 3  # Three of a kind
        else:
            score = 2  # Two pairs
    elif len(common) == 4:  # One pair
        score = 1
    else:  # High card
        score = 0
    return Hand(cards=s, score=score, ranks=ranks)


def parse_hand_with_joker(s: str) -> Hand:
    card_ranks = "J23456789TQKA"
    hand = parse_hand(s, card_ranks=card_ranks)
    best_score = hand.score
    for c in card_ranks[1:]:
        new_hand = parse_hand(s.replace("J", c), card_ranks=card_ranks)
        best_score = max(best_score, new_hand.score)
    hand.best_score = best_score
    return hand


def parse_hand_and_bid(s: str) -> tuple[Hand, int]:
    fst, snd = s.split(" ")
    return parse_hand(fst), int(snd)


def part1(lines: list[str]):
    hands_and_bids: list[tuple[Hand, int]] = [parse_hand_and_bid(line) for line in lines]
    hands_and_bids.sort(key=lambda hb: (hb[0].score, hb[0].ranks))
    return sum(hb[1] * i for i, hb in enumerate(hands_and_bids, start=1))


def part2(lines: list[str]):
    hands_and_bids: list[tuple[Hand, int]] = []
    for line in lines:
        fst, snd = line.split(" ")
        hand, bid = parse_hand_with_joker(fst), int(snd)
        hands_and_bids.append((hand, bid))
    hands_and_bids.sort(key=lambda hb: (hb[0].best_score, hb[0].ranks))
    return sum(hb[1] * i for i, hb in enumerate(hands_and_bids, start=1))


def main():
    lines = get_day_input(7)
    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
