import random

import numpy as np

from .utils import _return_all_neighboring_locs, _draw, _return_neighboring_unoccupied_locs, _move, _return_neighboring_occupied_locs, _find_connected_components, _sample

def Dreg(curr_loc, env):
    
    # do something to a neighbor slot
    neighboring_locs = _return_all_neighboring_locs(curr_loc, env)
    neighbor = random.choice(neighboring_locs)

    if neighbor not in env.keys():
        if _draw(.30):  # create res with 30% chance
            env[neighbor] = ("Res", None)
        elif _draw(.01):  # or create a new dreg with 1% chance
            env[neighbor] = ("Dreg", None)
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
        e = ("Dreg", None)
        _move(curr_loc, next_loc, e, env)
    else:
        pass

    
def Res(curr_loc, env):
    e = ("Res", None)
    free_locs = _return_neighboring_unoccupied_locs(curr_loc, env)
    if free_locs:
        next_loc = random.choice(free_locs)
        _move(curr_loc, next_loc, e, env)
        

def Data(curr_loc, env):
    if _draw(0.20):
        e = ("Data", env[curr_loc][1])
        free_locs = _return_neighboring_unoccupied_locs(curr_loc, env)
        if free_locs:
            next_loc = random.choice(free_locs)
            _move(curr_loc, next_loc, e, env)
    

def Emitter(curr_loc, env):
    # if a neighbor is a res... turn it into (a) data or (b) Emitter
    
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    if neighbors:
        for neighbor in neighbors:
            if env[neighbor][0] == "Res":
                if _draw(.90):
                    env[neighbor] = ("Data", _sample())
                else:
                    env[neighbor] = ("Emitter", None)
                                
                
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
        if neighbor[0] == "Data":
            dist = 3
            
            # move it if data is greater
            if neighbor[1] > env[curr_loc][1]:
                
                # move data up and the left

                next_loc = (curr_loc[0] - dist, curr_loc[1] - dist)
                env[next_loc] = ("Data", neighbor[1])
                env.pop(right_loc)
                
                # sorter update its internal value
                env[curr_loc] = ("Sorter", neighbor[1])
            
            # if not... move data down and left
            else:
                next_loc = (curr_loc[0] + dist, curr_loc[1] - dist)
                env[next_loc] = ("Data", neighbor[1])
                env.pop(right_loc)

                
                
    # step 2 - convert all neighboring res into Sorters
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    if neighbors:
        for neighbor in neighbors:
            if env[neighbor][0] == "Res":
                env[neighbor] = ("Sorter", _sample())
    
    
    # step 3 - move if one of its neighbors is a Sorter
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    if neighbors:
        for neighbor in neighbors:
            if env[neighbor][0] == "Sorter":
                free_locs = _return_neighboring_unoccupied_locs(curr_loc, env)
                if free_locs:
                    next_loc = random.choice(free_locs)
                    e = ("Sorter", env[curr_loc][1])
                    _move(curr_loc, next_loc, e, env)
                    break
                else:
                    next_loc = curr_loc
                
    # step 4 - die if it's surrounded by too many sorters
    count = 0
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    if neighbors:
        for neighbor in neighbors:
            if env[neighbor][0] == "Sorter":
                count += 1
    if count > 3:
        env.pop(next_loc)  # it is a next_loc because it moved in step 3


def Oil(curr_loc, env):
    # step 1 - convert neighboring res into oil
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    if neighbors:
        for neighbor in neighbors:
            if env[neighbor][0] == "Res":
                env[neighbor] = ("Oil", None)
    
    # step 2 move if it's not surrounded by enough oil droplets
    # step 2a - count how many neighbors are oil droplets
    count = 0
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    if neighbors:
        for neighbor in neighbors:
            if env[neighbor][0] == "Oil":  # 6 is oil's id
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
                    element = ("Oil", None)
                    _move(curr_loc, potential_loc, element, env)
                    return True
    return True


def Force(curr_loc, env):
    free_locs = _return_neighboring_unoccupied_locs(curr_loc, env)
    if free_locs:
        loc = random.choice(free_locs)
        env[loc] = ("Force", None)
    
def Wind(curr_loc, env):
    
    # step 1 - if theres a kite, push it
    neighbors = _return_neighboring_occupied_locs(curr_loc, env)
    
    if neighbors:
        left_neighbors = [l for l in neighbors if l[1] < curr_loc[1]]
        if left_neighbors:
            for neighbor in left_neighbors:
                if env[neighbor][0] == "Kite":
                    kite_new_loc = (neighbor[0], neighbor[1] - 2)
                    element = ("Kite", None)
                    _move(neighbor, kite_new_loc, element, env)
                    env.pop(curr_loc)  # wind disappears after pushing
                elif env[neighbor][0] == 8:
                    env.pop(curr_loc)
            
        # if theres no kite, move itself
        else:
            free_locs = _return_neighboring_unoccupied_locs(curr_loc, env)
            if free_locs:
                left_locs = [l for l in free_locs if l[1] < curr_loc[1]]
                if left_locs:
                    next_loc = random.choice(left_locs)
                    element = (8, None)
                    _move(curr_loc, next_loc, element, env)
                    
    # no neighbors
    else:
        free_locs = _return_neighboring_unoccupied_locs(curr_loc, env)
        left_locs = [l for l in free_locs if l[1] < curr_loc[1]]
        if left_locs:
            next_loc = random.choice(left_locs)
            element = (8, None)
            _move(curr_loc, next_loc, element, env)
        else:
            env.pop(curr_loc)
                    
        
def Kite(curr_loc, env):
    pass