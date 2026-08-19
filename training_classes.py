from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class Test:
    number: int
    ALLOWED_NUMBERS: ClassVar[tuple] = (1, 2, 3, 4)

    def __post_init__(self):
        if self.number not in self.ALLOWED_NUMBERS:
            raise ValueError(f"Number must be on of {self.ALLOWED_NUMBERS!r}")


t = Test(4)

@dataclass(order=True)
class Card:
    sort_index: int = field(init=False, repr=True)  # the order of the fields is important for the comparison operations (gt, lt, ge, le). By putting sort_index fist, it is first used for the tuple comparison
    rank: int
    suit: int

    def __post_init__(self):
        self.sort_index = self.rank * self.suit

c1 = Card(1, 2)
c2 = Card(2, 3)
print(c1)
print(c2)
print(c1 < c2)
