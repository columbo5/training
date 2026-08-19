from __future__ import annotations

import random
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class Grid:
    points: tuple[Point, Point, Point]  # only three Points at all times
    jump_counter: int = 0
    point_history: list[tuple[int, int]] = field(default_factory=list)
    grid_history: ClassVar[list[Grid]] = list()  # class variable that stores all grids ever produced, to see different random walks

    def __post_init__(self):
        self.add_points_to_history()
        self.grid_history.append(self)

    @classmethod
    def generate_standard(cls) -> Grid:
        return Grid(points=(
            Point(0, 0),
            Point(0, 1),
            Point(1, 0),
        ))

    def add_points_to_history(self):
        for point in self.points:
            self.point_history.append((point.x, point.y))

    def visualize_history(self) -> None:
        # convert point history to dataframe
        df = pd.DataFrame(dict(
            x=[p[0] for p in self.point_history],
            y=[p[1] for p in self.point_history],
        ))

        # plot df
        fig = px.scatter(
            df,
            x="x",
            y="y",
        )

        fig.show()

    @classmethod
    def visualize_all_grids(cls) -> None:
        """
        Plots all created grids
        :return:
        """

        layout = go.Layout(dict(
            title="several grids",
            xaxis=dict(
                title="x",
                range=[-100, 100]
            ),
            yaxis=dict(
                title="y",
        range = [-100, 100]
        )))

        # collect traces
        traces = list()
        for i, g in enumerate(cls.grid_history):
            x = [t[0] for t in g.point_history]
            y = [t[1] for t in g.point_history]
            traces.append(go.Scatter(x=x, y=y, mode="markers", name=f"grid_{i}"))

        fig = go.Figure(traces, layout)
        fig.show()

    def random_jumps(self, count: int) -> None:
        for _ in range(count):
            self.jump_counter += 1

            # select two points randomly
            pivot_point, moving_point = random.sample(self.points, 2)

            # jump
            moving_point.jump(pivot_point)

            # add new position to jump history
            self.point_history.append((moving_point.x, moving_point.y))


@dataclass
class Point:
    x: int
    y: int

    def jump(self, reference: Point):
        self.x = 2 * reference.x - self.x
        self.y = 2 * reference.y - self.y


if __name__ == "__main__":

    for i in range(100):
        grid = Grid.generate_standard()
        grid.random_jumps(count=100)

    Grid.visualize_all_grids()
