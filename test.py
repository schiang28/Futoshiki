import numpy as np

with open("puzzle.txt") as f:
    file = f.read().splitlines()
file = np.array(file)
print(file[::2, ::2])
