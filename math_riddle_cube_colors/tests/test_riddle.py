# tests/test_riddle.py

from collections import Counter
from itertools import product
import pytest
from riddle import Cube, CubeGrid


@pytest.mark.parametrize(
    ("first_coordinate", "second_coordinate", "expected"),
    [
        ((0, 0, 0), (0, 0, 0), 0),
        ((0, 0, 0), (1, 0, 0), 1),
        ((0, 0, 0), (1, 1, 0), 2),
        ((0, 0, 0), (1, 2, 3), 14),
        ((3, 3, 3), (0, 0, 0), 27),
    ],
)
def test_squared_distance(
    first_coordinate,
    second_coordinate,
    expected,
) -> None:
    first = Cube(first_coordinate, "r")
    second = Cube(second_coordinate, "b")

    assert first.squared_distance(second) == expected
    assert second.squared_distance(first) == expected


def test_count_colors() -> None:
    grid = CubeGrid(
        cubes=(
            Cube((0, 0, 0), "r"),
            Cube((1, 0, 0), "r"),
            Cube((2, 0, 0), "g"),
        )
    )

    assert grid.count_colors() == Counter({"r": 2, "g": 1})


def test_count_squared_distances() -> None:
    grid = CubeGrid(
        cubes=(
            Cube((0, 0, 0), "r"),
            Cube((1, 0, 0), "r"),
            Cube((2, 0, 0), "r"),
        )
    )

    assert grid.count_squared_distances("r") == Counter({
        1: 2,
        4: 1,
    })


def test_missing_or_single_color_produces_no_pairs() -> None:
    grid = CubeGrid(
        cubes=(
            Cube((0, 0, 0), "r"),
        )
    )

    assert grid.count_squared_distances("r") == Counter()
    assert grid.count_squared_distances("g") == Counter()


def test_invalid_color_raises_value_error() -> None:
    grid = CubeGrid(cubes=())

    with pytest.raises(ValueError):
        grid.count_squared_distances("yellow")


def test_random_grid_structure() -> None:
    grid = CubeGrid.generate_random(seed=10)

    assert len(grid.cubes) == 64
    assert {cube.coordinate for cube in grid} == set(
        product(range(4), repeat=3)
    )
    assert {cube.color for cube in grid} <= set(CubeGrid.colors)


def test_same_seed_produces_same_grid() -> None:
    assert (
        CubeGrid.generate_random(seed=10)
        == CubeGrid.generate_random(seed=10)
    )


@pytest.mark.parametrize("seed", [0, 1, 10, 42, 100])
def test_every_same_color_pair_is_counted(seed: int) -> None:
    grid = CubeGrid.generate_random(seed)
    color_counts = grid.count_colors()

    for color in CubeGrid.colors:
        number_of_cubes = color_counts[color]
        expected_pairs = number_of_cubes * (number_of_cubes - 1) // 2

        actual_pairs = sum(
            grid.count_squared_distances(color).values()
        )

        assert actual_pairs == expected_pairs


def test_six_equal_pairs_condition() -> None:
    false_grid = CubeGrid(
        cubes=tuple(
            Cube((x, 0, 0), "r")
            for x in range(6)
        )
    )
    true_grid = CubeGrid(
        cubes=tuple(
            Cube((x, 0, 0), "r")
            for x in range(7)
        )
    )

    assert not false_grid.has_minimum_six_equal_color_equal_dist_pairs()
    assert true_grid.has_minimum_six_equal_color_equal_dist_pairs()


def test_grid_iteration() -> None:
    cubes = (
        Cube((0, 0, 0), "r"),
        Cube((1, 0, 0), "g"),
    )
    grid = CubeGrid(cubes)

    assert tuple(grid) == cubes
