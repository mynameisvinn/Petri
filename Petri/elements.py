import random

import numpy as np

from .utils import _return_all_neighboring_locs, _draw, _return_neighboring_unoccupied_locs, _move, _return_neighboring_occupied_locs, _find_connected_components, _sample

def Dreg(curr_loc, env):
    
    # do something to a neighbor slot
    neighboring_locs = _return_all_neighboring_locs(curr_loc, env)
    neighbor = random.choice(neighboring_locs)

    if neighbor not in env.keys():
        if _draw(.30):  # create res with 30% chance
            env[neighbor] = (2, None)
        elif _draw(.01):  # or create a new dreg with 1% chance
            env[neighbor] = (1, None)
        else:
            pass
    
    # if dreg is next to a occupied slot, randomly destroy neighborhood
    else:
        if _draw(.2):
            neighbors = _return_neighboring_occupied_locs(curr_loc, env)
            for neighbor in neighbors:
                env.pop(neighbor)

    # move to an unoccupied slot (or stay put if there are no unoccupied slots)
    open_locs = _return_neighboring_unoccupied_locs(curr_loc, env)
    if open_locs:
        next_loc = random.choice(open_locs)
        e = (1, None)
        _move(curr_loc, next_loc, e, env)
    else:
        pass

    
def Res(curr_loc, env):
    e = (2, None)
    free_locs = _return_neighboring_unoccupied_locs(curr_loc, env)
    if free_locs:
        next_loc = random.choice(free_locs)
        _move(curr_loc, next_loc, e, env)
        

def Data(curr_loc, env):
    if _draw(0.20):
        e = (4, env[curr_loc][1])
        free_locs = _return_neighboring_unoccupied_locs(curr_loc, env)
        if free_locs:
            next_loc = random.choice(free_locs)
            _move(curr_loc, next_loc, e, env)
    

def Emitter(curr_loc, env):
    # if a neighbor is a res... turn it into (a) data or (b) Emitter
    
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    if neighbors:
        for neighbor in neighbors:
            if env[neighbor][0] == 2:
                if _draw(.90):
                    env[neighbor] = (4, _sample())
                else:
                    env[neighbor] = (5, None)
                                
                
def Sorter(curr_loc, env):
    """
    In  this  version, Sorter has two primary functions. 
    
    First, whenever it sees a Res, it transmutes it into another Sorter, and so 
    the Sorter population  level  is indirectly  controlled  by DReg.
    
    Secondly, Sorter transports Datums from right to left when possible, and also up 
    or down based on the comparison of the Datum’s value with a 32-bit threshold stored 
    in the Sorter. 
    
    When a Datum ‘crosses’ the Sorter during  a  move,  the Sorter copies  the Datum’s  
    value  to  its  threshold
    """
    right_loc = (curr_loc[0], curr_loc[1] + 1)
    
    # step 1 - move data... if theres something to its right
    if right_loc in env.keys():
        neighbor = env[right_loc]
        
        # we only want data elements...
        if neighbor[0] == 4:
            dist = 3
            
            # move it if data is greater
            if neighbor[1] > env[curr_loc][1]:
                
                # move data up and the left

                next_loc = (curr_loc[0] - dist, curr_loc[1] - dist)
                env[next_loc] = (4, neighbor[1])
                env.pop(right_loc)
                
                # sorter update its internal value
                env[curr_loc] = (3, neighbor[1])
            
            # if not... move data down and left
            else:
                next_loc = (curr_loc[0] + dist, curr_loc[1] - dist)
                env[next_loc] = (4, neighbor[1])
                env.pop(right_loc)

                
                
    # step 2 - convert all neighboring res into Sorters
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    if neighbors:
        for neighbor in neighbors:
            if env[neighbor][0] == 2:
                env[neighbor] = (3, _sample())
    
    
    # step 3 - move if one of its neighbors is a Sorter
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    if neighbors:
        for neighbor in neighbors:
            if env[neighbor][0] == 3:
                free_locs = _return_neighboring_unoccupied_locs(curr_loc, env)
                if free_locs:
                    next_loc = random.choice(free_locs)
                    e = (3, env[curr_loc][1])
                    _move(curr_loc, next_loc, e, env)
                    break
                else:
                    next_loc = curr_loc
                
    # step 4 - die if it's surrounded by too many sorters
    count = 0
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    if neighbors:
        for neighbor in neighbors:
            if env[neighbor][0] == 3:
                count += 1
    if count > 3:
        env.pop(next_loc)  # it is a next_loc because it moved in step 3


def Oil(curr_loc, env):
    # step 1 - convert neighboring res into oil
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    if neighbors:
        for neighbor in neighbors:
            if env[neighbor][0] == 2:
                env[neighbor] = (6, None)
    
    # step 2 move if it's not surrounded by enough oil droplets
    # step 2a - count how many neighbors are oil droplets
    count = 0
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    if neighbors:
        for neighbor in neighbors:
            if env[neighbor][0] == 6:  # 6 is oil's id
                count += 1

    # find its blob, which includes itself
    connected_components = _find_connected_components(curr_loc, env)
    for component in connected_components:
        
        # return empty locs surrounding the blob
        unoccupied_locs = _return_neighboring_unoccupied_locs(component, env)
        if unoccupied_locs:
            for potential_loc in unoccupied_locs:
                potential_neighbors = _return_neighboring_occupied_locs(potential_loc, env)
                if len(potential_neighbors) > count:
                    element = (6, None)
                    _move(curr_loc, potential_loc, element, env)
                    return True
    return True