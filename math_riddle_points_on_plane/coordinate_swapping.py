from __future__ import annotations

import random
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dataclasses import dataclass, field


# TYPE DEFINITIONS
Coordinate = tuple[int, int]
GridState = tuple[Coordinate, Coordinate, Coordinate]
GridHistory = list[GridState]


# CLASS DEFINTIONS
@dataclass(slots=True)
class Grid:
    points: tuple[Point, Point, Point]  # only three Points at all times

    # these are always the same, so should/must not be specifiable as parameters during instantiation (so init=False)
    history: GridHistory = field(
        default_factory=list,
        init=False,
        repr=False)

    def __post_init__(self) -> None:

        # validity checks
        if len(self.points) != 3:
            raise ValueError(f"expected 3 points, got {len(self.points)}")

        # check for duplicates with identical coordinates
        coordinates = tuple(
            p.coordinate for p in self.points
        )
        if len(set(coordinates)) != len(coordinates):
            raise ValueError(f"coordinates must be unique, got {coordinates}")

        self.add_grid_state_to_history()  # initial state after creation

    @classmethod
    def generate_standard(cls) -> Grid:
        return cls(points=(
            Point(0, 0),
            Point(0, 1),
            Point(1, 0),
        ))

    def generate_grid_state(self) -> GridState:
        first, second, third = self.points

        return (
            first.coordinate,
            second.coordinate,
            third.coordinate
        )

    def add_grid_state_to_history(self) -> None:
        self.history.append(self.generate_grid_state())

    def random_jumps(self, count: int, *, rng: random.Random | None = None) -> None:

        if count < 0:
            raise ValueError(f"Count is {count}, but must be >= 0")

        if rng is None:  # random-ness should be controllable via a seed if desired. This makes testing possible
            rng = random.Random()

        for _ in range(count):
            # select two points randomly
            pivot_point, moving_point = rng.sample(self.points, 2)

            # jump
            moving_point.jump(pivot_point)

            # add new state to history
            self.add_grid_state_to_history()

    def convert_history_to_point_df(self) -> pd.DataFrame:
        result = [
            dict(
                iteration=i,
                point_no=j,
                x=coord[0],
                y=coord[1]
            )
            for i, state in enumerate(self.history)
            for j, coord in enumerate(state)
        ]
        df = pd.DataFrame.from_records(result)

        return df

    def visualize_history(self) -> go.Figure:
        df = self.convert_history_to_point_df()

        # plot df
        fig = px.scatter(
            df,
            x="x",
            y="y",
        )

        return fig


@dataclass(slots=True)
class Point:
    x: int
    y: int

    def __post_init__(self) -> None:
        if type(self.x) != int or type(self.y) != int:
            raise TypeError(f"expected int for both x and y, got {type(self.x)}")

    @property
    def coordinate(self) -> Coordinate:
        return self.x, self.y

    def jump(self, reference: Point) -> None:
        self.x = 2 * reference.x - self.x
        self.y = 2 * reference.y - self.y


# FUNCTIONS
def visualize_all_grids(grid_collection: list[Grid]) -> go.Figure:

    layout = dict(
        title="several grids",
        xaxis=dict(
            title="x",
            range=[-100, 100],
            autorange=False,
            constrain="domain"
        ),
        yaxis=dict(
            title="y",
            range=[-100, 100],
            scaleanchor="x",
            scaleratio=1,
            autorange=False,
            constrain="domain"
    ))

    # collect traces
    traces = list()
    for i, g in enumerate(grid_collection):
        df = g.convert_history_to_point_df()
        traces.append(go.Scatter(x=df["x"], y=df["y"], mode="markers", name=f"grid_{i}"))

    fig = go.Figure(traces, layout)
    return fig

def run_experiment(grid_count: int, jump_count: int, rng: random.Random | None = None) -> list[Grid]:

    grid_collection: list[Grid] = []  # to capture the grids here and not as class variable in Grid is better, so the instances do not alter the class state.
    for _ in range(grid_count):
        grid = Grid.generate_standard()
        grid.random_jumps(count=jump_count, rng=rng)
        grid_collection.append(grid)

    return grid_collection

def main():

    # run settings
    GRID_COUNT = 10
    GRID_JUMP_COUNT = 50
    rng = random.Random(42)

    # run experiment
    grid_collection = run_experiment(GRID_COUNT, GRID_JUMP_COUNT, rng)

    # visualization
    fig = visualize_all_grids(grid_collection)
    fig.show()

if __name__ == "__main__":

    main()