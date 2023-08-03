import numpy as np

# possible positions in each bthread ([1, 2, 3])
P = np.array([
    [0, 0, 0],
    [0, 1, 0],
    [0, 2, 0],  # unsolvable
    [0, 3, 0],  # unsolvable
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1],
    [1, 2, 0],
    [1, 2, 1],  # unsolvable
    [1, 3, 0],  # unsolvable
    [1, 3, 1],  # unsolvable
    [2, 1, 1],
    [2, 2, 0],
    [2, 2, 1],
    [2, 3, 0],
    [2, 3, 1],  # unsolvable
    [3, 2, 1],
    [3, 3, 0],
    [3, 3, 1],
])

# desired events for each position ([H, C, I])
Y = np.array([
    [1, 1, 0],
    [1, 0, 0],
    [0, 0, 0],  # unsolvable
    [0, 0, 0],  # unsolvable
    [0, 1, 0],
    [1, 1, 0],
    [0, 1, 0],
    [1, 0, 0],
    [0, 0, 0],  # unsolvable
    [0, 0, 0],  # unsolvable
    [0, 0, 0],  # unsolvable
    [0, 1, 0],
    [1, 1, 0],
    [0, 1, 0],
    [1, 0, 1],
    [0, 0, 0],  # unsolvable
    [0, 1, 0],
    [0, 0, 1],
    [0, 0, 1],
])