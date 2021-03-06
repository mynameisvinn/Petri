import random

import numpy as np

from .utils import _draw, _return_random_loc, _sample


def create_wind(n_rows, n_cols, n_force, n_kites):
    world = {}
    world['n_rows'] = n_rows
    world['n_cols'] = n_cols
            
    for _ in range(n_force):
        i = random.choice(np.arange(n_rows))
        j = random.choice(np.arange(n_cols - (n_cols // 5), n_cols))  # the right fifth of the board
        loc = (i, j)
        world[loc] = (7, None)
        
    for _ in range(n_kites):
        loc = _return_random_loc(n_rows, n_cols)
        world[loc] = (1, None)    
    return world


def create_oil_world(n_rows, n_cols, n_dregs, n_oil):
    world = {}
    world['n_rows'] = n_rows
    world['n_cols'] = n_cols
    
    # create dregs
    for _ in range(n_dregs):
        loc = _return_random_loc(n_rows, n_cols)
        world[loc] = ("Dreg", None)
        
    # create oil (represented by id 6)
    for _ in range(n_oil):
        loc = _return_random_loc(n_rows, n_cols)
        world[loc] = ("Oil", None)
    return world


def create_sorting_world(n_rows, n_cols, n_dregs, n_sorters, n_emitters):
    """initialize world for sorting numbers.
    """
    world = {}
    world['n_rows'] = n_rows
    world['n_cols'] = n_cols    
    
    # create dregs (represented by id 1)
    for _ in range(n_dregs):
        loc = _return_random_loc(n_rows, n_cols)
        world[loc] = ("Dreg", None)
        
    # create sorter (represented by id 3)
    for _ in range(n_sorters):
        loc = _return_random_loc(n_rows, n_cols)
        world[loc] = ("Sorter", _sample())
        
    
    # create emitter (represented by id 5)
    for _ in range(n_emitters):
        i = random.choice(np.arange(n_rows))
        j = random.choice(np.arange(n_cols - (n_cols // 5), n_cols))  # the right fifth of the board
        loc = (i, j)
        world[loc] = ("Emitter", None)
    return world