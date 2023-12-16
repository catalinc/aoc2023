#!/usr/bin/env python3
from collections import defaultdict
from dataclasses import dataclass
from multiprocessing import Pool
from typing import Iterable

from astar import AStar

from utils import get_day_input_full_content


@dataclass(order=True)
class Pixel:
    row: int
    col: int

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))


@dataclass
class Image:
    height: int
    width: int
    galaxies: list[Pixel]
    space: set[Pixel]
    expansion: int = 0

    def neighbours(self, pixel: Pixel) -> list[Pixel]:
        ret = []
        if pixel.row > 0:
            ret.append(Pixel(row=pixel.row - 1, col=pixel.col))
        if pixel.row < self.height - 1:
            ret.append(Pixel(row=pixel.row + 1, col=pixel.col))
        if pixel.col > 0:
            ret.append(Pixel(row=pixel.row, col=pixel.col - 1))
        if pixel.col < self.width - 1:
            ret.append(Pixel(row=pixel.row, col=pixel.col + 1))
        return ret

    def min_distance(self, start: Pixel, end: Pixel) -> int:
        path = ImageAStar(self).astar(start=start, goal=end, reversePath=True)
        return sum(self.expansion if n in self.space else 1 for n in path) - 1

    def min_distances(self, index: int) -> tuple[int, dict[int, int]]:
        galaxy = self.galaxies[index]
        distances = {}
        for i in range(index + 1, len(self.galaxies)):
            goal = self.galaxies[i]
            dist = self.min_distance(galaxy, goal)
            distances[i] = dist
        return index, distances


class ImageAStar(AStar):
    def __init__(self, image: Image):
        self.image = image

    def heuristic_cost_estimate(self, current: Pixel, goal: Pixel) -> float:
        return abs(goal.row - current.row) + abs(goal.col - current.col)

    def distance_between(self, n1: Pixel, n2: Pixel) -> float:
        return 1

    def neighbors(self, node: Pixel) -> Iterable[Pixel]:
        return self.image.neighbours(node)

    def is_goal_reached(self, current: Pixel, goal: Pixel) -> bool:
        return current == goal


def parse_image(s: str) -> Image:
    galaxies = []
    empty = {"rows": defaultdict(int), "cols": defaultdict(int)}
    lines = [line for line in s.split("\n") if line]
    for row, line in enumerate(lines):
        for col, ch in enumerate(line):
            if ch == "#":
                g = Pixel(row=row, col=col)
                galaxies.append(g)
            else:
                empty["rows"][row] += 1
                empty["cols"][col] += 1
    width = len(lines[0])
    space = set()
    for row, cnt in empty["rows"].items():
        if cnt == width:
            for col in range(width):
                space.add(Pixel(row=row, col=col))
    height = len(lines)
    for col, cnt in empty["cols"].items():
        if cnt == len(lines):
            for row in range(height):
                space.add(Pixel(row=row, col=col))
    return Image(
        height=height,
        width=width,
        galaxies=galaxies,
        space=space,
    )


def compute_total_distance(image: Image, expansion: int = None) -> int:
    if expansion:
        image.expansion = expansion
    with Pool() as pool:
        results = pool.map(image.min_distances, range(len(image.galaxies) - 1))
    total = 0
    for _, distances in results:
        for d in distances.values():
            total += d
    return total


def part1(image: Image) -> int:
    return compute_total_distance(image, expansion=2)


def part2(image: Image) -> int:
    return compute_total_distance(image, expansion=1000000)


def main():
    s = get_day_input_full_content(11)
    image = parse_image(s)
    print(part1(image))
    print(part2(image))


if __name__ == "__main__":
    main()
