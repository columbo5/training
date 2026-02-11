


a: int = 2

print(a)

# %% 

import collections

Card = collections.namedtuple("Card", ["rank", "suit"])

class Frenchdeck:
    ranks = [str(i) for i in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs heards".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
    
    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position]
    
# %%
card1 = Frenchdeck()

# %%

# card1.__len__()
len(card1)
deck = Frenchdeck()
deck[2]

#%%

for i in reversed([1, 2, 3]):
    print(i)

#%%

import doctest

def testfunc(x):
    return 2*x

#%%

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        import math
        return math.sqrt(self.x **2 + self.y ** 2)
    
    def __add__(self, vector2):
        new_x = self.x + vector2.x
        new_y = self.y + vector2.y

        return Vector(new_x, new_y)
    
    def __repr__(self):
        return " ".join(["Vector:", "x=", str(self.x), ", y=", str(self.y)])

    def __str__(self):
        return self.__repr__()
    

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2  # test
print(v3)
#%%

def matching(var: int):
    match searching := [int(i) for i in tuple(str(var))]:
        case list(test):
            print("first")
            print(test)
        case 3 if True:
            print("y")
        case R"\d+" as other:
            print(other)
        case [5, *other]:
            print("X")
            print(other)
        case _:
            print("else", searching)

matching(534)

#%%
tuple(str(123))

#%%

middle = slice(2, 5, 1)
all = [1, 2, 3, 4, 5, 6, 7]
print(all[middle])
#%%
import numpy as np
fdl = np.array([
    [1, 2],
    [1, 2],
    [1, 2],
])

fdl[..., 1]
...
#%%

a = 10
b = [1, a, 3]
print("b", b)
b[1] = 40
print("b", b)
print("a", a)
#%%
a: tuple = (1, 2)
print(id(a))
a *= 2
print(a)
print(id(a))

#%%

import bisect

a: list = [1, 3, 5, 3, 6, 7]
print(a)
a.sort()
print(a)
bisect.insort(a, 2)
print(a)
#%%

from array import array

a: array = array("L", (i for i in range(int(1e8))))
#%%
a[10]

b = (i for i in range(int(1e8)))

c = list(b)