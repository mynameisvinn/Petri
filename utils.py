import random

import numpy as np

def _return_random_loc(n_rows, n_cols):
    i = random.choice(np.arange(n_rows))
    j = random.choice(np.arange(n_cols))
    return (i, j)


def update_canvass(canvass, env, n_rows, n_cols):
    """update numpy matrix given world.
    """
    canvass[:] = 0
    for i in range(n_rows):
        for j in range(n_cols):
            loc = (i, j)
            if loc in env.keys():
                canvass[i][j] = env[loc][0]
    return canvass


def _draw(prob):
    return np.random.uniform() > (1 - prob)


def _summarize(w):
    """tabulate elements in world.
    """
    count = {}
    for i, j in w.values():
        if i not in count.keys():
            count[i] = 1
        else:
            count[i] += 1
    print(count)    