#!/usr/bin/env python3
from collections import namedtuple, deque
from dataclasses import dataclass, field
from itertools import product
from typing import ClassVar

from utils import get_day_input_full_content

Tile = namedtuple("Tile", ["shape", "row", "col"])


@dataclass
class PipeMap:
    grid: list[list[Tile]]
    start: Tile
    loop: list[Tile] = field(init=False)
    FITTINGS: ClassVar[dict[str, str]] = {
        "N": "|F7",
        "S": "|JL",
        "E": "-7J",
        "W": "-FL"
    }
    SHAPES: ClassVar[dict[str, str]] = {
        "|": "NS",
        "-": "EW",
        "L": "NE",
        "J": "NW",
        "7": "SW",
        "F": "SE"
    }

    def __post_init__(self):
        shape = self.find_fitting_shape(self.start)
        _, row, col = self.start
        self.start = Tile(shape, row, col)
        self.grid[row][col] = self.start
        self.loop = self._find_loop()

    def get_neighbours(self, tile: Tile) -> dict[str, Tile]:
        _, row, col = tile
        ret = {}
        if row > 0:
            ret["N"] = self.grid[row - 1][col]
        if row < len(self.grid) - 1:
            ret["S"] = self.grid[row + 1][col]
        if col > 0:
            ret["W"] = self.grid[row][col - 1]
        if col < len(self.grid[0]) - 1:
            ret["E"] = self.grid[row][col + 1]
        return ret

    def find_fitting_shape(self, tile: Tile) -> str:
        neighbours = self.get_neighbours(tile)
        for shape, orientations in self.SHAPES.items():
            fst, snd = orientations[0], orientations[1]
            if fst in neighbours and neighbours[fst].shape in self.FITTINGS[fst] \
                    and snd in neighbours and neighbours[snd].shape in self.FITTINGS[snd]:
                return shape

    def find_fitting_neighbours(self, tile: Tile) -> list[Tile]:
        orientation = self.SHAPES[tile.shape]
        fst, snd = orientation[0], orientation[1]
        neighbours = self.get_neighbours(tile)
        fitting = []
        if fst in neighbours and neighbours[fst].shape in self.FITTINGS[fst]:
            fitting.append(neighbours[fst])
        if snd in neighbours and neighbours[snd].shape in self.FITTINGS[snd]:
            fitting.append(neighbours[snd])
        return fitting

    def _find_loop(self):
        loop: list[Tile] = [self.start]
        while True:
            curr = loop[-1]
            for n in self.find_fitting_neighbours(curr):
                # need at least three tiles to form a loop
                if len(loop) >= 3 and n == self.start:
                    return loop
                if n not in loop:
                    # assume there can be only one path
                    loop.append(n)
                    break


def parse_pipe_map(s: str) -> PipeMap:
    grid: list[list[Tile]] = []
    for row, line in enumerate(s.split("\n")):
        grid.append([])
        for col, shape in enumerate(list(line)):
            grid[-1].append(Tile(shape, row, col))
    for i, j in product(range(len(grid)), range(len(grid[0]))):
        if grid[i][j].shape == "S":
            return PipeMap(grid=grid, start=grid[i][j])


def debug_print(pm: PipeMap):
    screen = []
    for row in pm.grid:
        line = []
        for t in row:
            if t in pm.loop:
                line.append("*")
            else:
                line.append(t.shape)
        screen.append("".join(line))
    print("\n".join(screen))


def part1(pm: PipeMap) -> int:
    return len(pm.loop) // 2


def part2(pm: PipeMap) -> int:
    debug_print(pm)
    # find tiles inside the loop, the do flood fill
    inside: set[Tile] = set()
    for tile in pm.loop:
        if tile.shape == "L":
            t = pm.grid[tile.row - 1][tile.col + 1]
            if t not in pm.loop:
                inside.add(t)
        if tile.shape == "J":
            t = pm.grid[tile.row - 1][tile.col - 1]
            if t not in pm.loop:
                inside.add(t)
        if tile.shape == "F":
            t = pm.grid[tile.row + 1][tile.col + 1]
            if t not in pm.loop:
                inside.add(t)
        if tile.shape == "7":
            t = pm.grid[tile.row - 1][tile.col - 1]
            if t not in pm.loop:
                inside.add(t)
    area: set[Tile] = set()
    to_visit = deque(inside)
    while to_visit:
        curr = to_visit.popleft()
        area.add(curr)
        for n in pm.get_neighbours(curr).values():
            if n in area:
                continue
            if n in pm.loop:
                continue
            to_visit.append(n)
    return len(area)


def main():
    s = get_day_input_full_content(10)
    pm = parse_pipe_map(s)
    print(part1(pm))
    print(part2(pm))


if __name__ == "__main__":
    main()
