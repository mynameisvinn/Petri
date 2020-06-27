import random

import numpy as np

def _move(curr_loc, next_loc, element, env):
    """move element from curr_loc to next_loc.
    """
    if next_loc != curr_loc:
        env[next_loc] = element
        env.pop(curr_loc)
        return True
    return False


def _return_random_loc(n_rows, n_cols):
    i = random.choice(np.arange(n_rows))
    j = random.choice(np.arange(n_cols))
    return (i, j)


def _draw(prob):
    return np.random.uniform() > (1 - prob)


def summarize(env):
    """tabulate elements in world.
    """
    count = {}
    for k, v in env.items():
        if isinstance(k, tuple):
            if v[0] not in count.keys():
                count[v[0]] = 1
            else:
                count[v[0]] += 1
    return count


def _return_all_neighboring_locs(loc, env):
    """return neighboring locs, occupied or unoccupied
    """
    n_rows = env["n_rows"]
    n_cols = env["n_cols"]
    
    i = loc[0]
    j = loc[1]
    neighboring_locs = [(min(i + 1, n_rows - 1), j), 
                        (max(i - 1, 0), j), 
                        (i, min(j + 1, n_cols - 1)), 
                        (i, max(j - 1, 0))]
    
    neighboring_locs = [l for l in neighboring_locs if l != loc]  # check that neighbor is not itself
    return neighboring_locs


def _return_neighboring_occupied_locs(loc, env):
    """return all locs that are occupied.
    """
    neighboring_locs = _return_all_neighboring_locs(loc, env)
    return [loc for loc in neighboring_locs if loc in env.keys()]


def _return_neighboring_unoccupied_locs(loc, env):
    """return all locs that are unoccupied.
    """
    neighboring_locs = _return_all_neighboring_locs(loc, env)
    return [loc for loc in neighboring_locs if loc not in env.keys()]


def _sample():
    """draw a sample to populate sorters and emitters.
    """
    return np.random.randint(0, 100)


def take_first(elem):
    return elem[0]


def _find_connected_components(curr_loc, env):
    """return list of oil droplets that are connected to curr.
    """

    stack = [curr_loc]
    visited = []

    while stack:
        curr = stack.pop()
        visited.append(curr)

        search_grid = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (j == 0) and (i == 0):
                    pass
                else:
                    search_grid.append((curr[0] + i, curr[1] + j))

        for grid in search_grid:
            if grid in env.keys() and (grid not in visited) and (grid not in stack):
                if env[grid][0] == 6:
                    stack.append(grid)
    return sorted(visited, key = lambda x: x[0])

def _scatter(curr_loc, env):
    """move element to an unoccupied location.
    """
    free_locs = _return_neighboring_unoccupied_locs(curr_loc, env)
    if free_locs:
        next_loc = random.choice(free_locs)
        _move(curr_loc, next_loc, env[curr_loc], env)
        return next_loc, env  # next_loc is the new curr_loc
    return curr_loc, env
        
def _replicate(curr_loc, env):
    """replicate if there are neighboring res.
    """
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    if neighbors:
        for neighbor in neighbors:
            if env[neighbor][0] == "Res":
                env[neighbor] = env[curr_loc]
    return curr_loc, env