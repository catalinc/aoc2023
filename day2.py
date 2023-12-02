#!/usr/bin/env python3


import regex as re
from collections import defaultdict
from utils import get_day_input


class Game:
    def __init__(self, gid: int) -> None:
        self.id: int = gid
        self.rounds: list[dict[str, int]] = []


def parse_game_round(s: str) -> dict[str, int]:
    game_round = defaultdict(int)
    cubes = re.findall(r"(\d+) (\w+)", s)
    for p in cubes:
        count, color = int(p[0]), p[1]
        game_round[color] = count
    return game_round


def parse_game(s: str) -> Game:
    head, tail = s.split(":")
    gid = int(re.findall(r"\d+", head)[0])
    game = Game(gid)
    for section in tail.split(";"):
        game.rounds.append(parse_game_round(section))
    return game


def is_possible(game: Game, max_cubes: dict[str, int]) -> bool:
    for game_round in game.rounds:
        if game_round["red"] > max_cubes["red"]:
            return False
        if game_round["green"] > max_cubes["green"]:
            return False
        if game_round["blue"] > max_cubes["blue"]:
            return False
    return True


def power_min_cubes(game: Game) -> int:
    min_red, min_green, min_blue = 0, 0, 0
    for game_round in game.rounds:
        min_red = max(min_red, game_round["red"])
        min_green = max(min_green, game_round["green"])
        min_blue = max(min_blue, game_round["blue"])
    return min_red * min_green * min_blue


def part1(games: list[Game]) -> int:
    max_cubes = {
        "red": 12,
        "green": 13,
        "blue": 14
    }
    return sum(g.id for g in games if is_possible(g, max_cubes))


def part2(games: list[Game]) -> int:
    return sum(power_min_cubes(g) for g in games)


def main():
    lines = get_day_input(2)
    games = [parse_game(line) for line in lines]
    print(part1(games))
    print(part2(games))


if __name__ == "__main__":
    main()
