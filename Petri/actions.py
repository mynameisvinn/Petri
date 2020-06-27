import random

from .utils import _return_neighboring_unoccupied_locs, _move, _return_neighboring_occupied_locs, _move


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