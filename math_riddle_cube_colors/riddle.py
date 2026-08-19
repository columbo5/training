from __future__ import annotations
from random import choice
from itertools import product, combinations
from dataclasses import dataclass
from collections import Counter
from typing import ClassVar
import math
from random import Random
from collections.abc import Iterator

# define type aliases
Coordinate = tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class Cube:
    coordinate: Coordinate
    color: str

    def squared_distance(self, other: Cube) -> int:
        distance = sum(
            (i - j)**2 for i, j in zip(other.coordinate, self.coordinate)
        )
        return distance


@dataclass(frozen=True)
class CubeGrid:

    cubes: tuple[Cube, ...]
    colors: ClassVar[tuple[str, str, str]] = ("r", "g", "b")

    @classmethod
    def generate_random(cls, seed: int | None = None) -> CubeGrid:  # generates cubeGrid instance

        rng = Random(seed)

        # generate 64 cubes
        coordinate_register: list[Coordinate] = list(product(range(4), repeat=3))
        assert len(coordinate_register) == 64

        cubes = tuple(
            Cube(
                coordinate=coordinate,
                color=rng.choice(cls.colors)
            )
            for coordinate in coordinate_register
        )

        return cls(cubes)

    def count_colors(self) -> Counter[str]:
        return Counter(cube.color for cube in self.cubes)

    def count_squared_distances(self, color: str) -> Counter[int]:
        # assert color in type(self).colors, f"color must be one of {type(self).colors}" apparently, assertions are used for internal checks, not for validation of user input

        if color not in type(self).colors:
            raise ValueError(f"Color must be one of {type(self).colors}")

        same_color_cubes = (i for i in self.cubes if i.color == color)  # genexp
        dist_counter = Counter(i.squared_distance(j) for i, j in combinations(same_color_cubes, 2))

        return dist_counter


    def has_minimum_six_equal_color_equal_dist_pairs(self) -> bool:
        return any(
            max(self.count_squared_distances(color).values(), default=0) >= 6 for color in type(self).colors

        )

    def __iter__(self) -> Iterator[Cube]:
        return iter(self.cubes)

