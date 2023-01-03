import sys
import math
from dataclasses import dataclass

ME = 1
OPP = 0
NONE = -1

@dataclass
class Tile:
    x: int
    y: int
    scrap_amount: int
    owner: int
    units: int
    recycler: bool
    can_build: bool
    can_spawn: bool
    in_range_of_recycler: bool

width, height = [int(i) for i in input().split()]

# Functions
def optimize_recycler(my_tiles):
    max_scrap_amount = 0
    location_tile = Tile(-1,-1,-1,-1,-1,False,False,False,False)
    for my_tile in my_tiles:
        #check for nearby tiles:
        if (my_tile.scrap_amount >= max_scrap_amount) & (my_tile.units == 0):
            max_scrap_amount = my_tile.scrap_amount
            location_tile = my_tile
    
    return location_tile

def optimize_spawn():
    return 1

def find_path():
    #find among a neutral_tiles that has the highest scrap amount
    highest_scrap_amount = 1
    for neutral_tile in neutral_tiles:
        
        if neutral_tile.scrap_amount > highest_scrap_amount & neutral_tile.in_range_of_recycler!=1:
            path_x = neutral_tile.x
            path_y = neutral_tile.y
            highest_scrap_amount = neutral_tile.scrap_amount
    
    return path_x, path_y

def find_path_1step(current_tile):
    path_options = []
    decision_path = current_tile
    # priority 1:  step on enemy path
    for opp_tile in opp_tiles:
        if opp_tile.x == current_tile.x or opp_tile.y == current_tile.y:
            path_options.append(opp_tile)

    # priority 2: natural tiles that has higher
    if len(path_options) == 0:
        for neutral_tile in neutral_tiles:
            if neutral_tile.x == current_tile.x or neutral_tile.y == current_tile.y:
                path_options.append(neutral_tile)

    # priorty 3:
    # if len(path_options) == 0:
    # Choose the best based on the highest scrap_amount


    highest_scrap_amount = 0
    for path in path_options:
        if path.scrap_amount >= highest_scrap_amount:
            print("Higher scrap amount!: ", path ,file=sys.stderr, flush=True)
            highest_scrap_amount = path.scrap_amount
            decision_path = path

    # print("current_tile: ", current_tile ,file=sys.stderr, flush=True)
    # print("Decision_path: ", decision_path ,file=sys.stderr, flush=True)

    return decision_path.x, decision_path.y


def find_path_recycler(opp_recyclers):
    for opp_recycler in opp_recyclers:
        highest_scrap_amount = 1
        if opp_recycler.scrap_amount > highest_scrap_amount & opp_recycler.in_range_of_recycler!=1:
            path_x = opp_recycler.x
            path_y = opp_recycler.y
            highest_scrap_amount = opp_recycler.scrap_amount
    
    return opp_recycler.x, opp_recycler.y



# game loop
while True:
    tiles = []
    my_units = []
    opp_units = []
    my_recyclers = []
    opp_recyclers = []
    opp_tiles = []
    my_tiles = []
    neutral_tiles = []

    my_matter, opp_matter = [int(i) for i in input().split()]
    for y in range(height):
        for x in range(width):
            # owner: 1 = me, 0 = foe, -1 = neutral
            # recycler, can_build, can_spawn, in_range_of_recycler: 1 = True, 0 = False
            scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [int(k) for k in input().split()]
            tile = Tile(x, y, scrap_amount, owner, units, recycler == 1, can_build == 1, can_spawn == 1, in_range_of_recycler == 1)

            tiles.append(tile)

            if tile.owner == ME:
                my_tiles.append(tile)
                if tile.units > 0:
                    my_units.append(tile)
                elif tile.recycler:
                    my_recyclers.append(tile)
            elif tile.owner == OPP:
                opp_tiles.append(tile)
                if tile.units > 0:
                    opp_units.append(tile)
                elif tile.recycler:
                    opp_recyclers.append(tile)
            else:
                neutral_tiles.append(tile)

    actions = []
    
    # Should I build the recycler and where
    if len(my_recyclers) == 0:
        recycler_loc = optimize_recycler(my_tiles)
        actions.append('BUILD {} {}'.format(recycler_loc.x, recycler_loc.y))

    for tile in my_tiles:
        if tile.can_spawn:
            # Check of we should spawn here
            
            amount = optimize_spawn() # TODO: pick amount of robots to spawn here
            if amount > 0:
                actions.append('SPAWN {} {} {}'.format(amount, tile.x, tile.y))
        # if tile.can_build:
            
        #     should_build = optimize_recycler(len(my_recyclers), tile) # TODO: pick whether to build recycler here
        #     if should_build:
        #         actions.append('BUILD {} {}'.format(tile.x, tile.y))

    for tile in my_units:
        # Find the path that has the highest scrap_amount
        target = True
        # target_x, target_y = find_path_recycler(opp_recyclers) # TODO: pick a destination tile
        # target_x, target_y = find_path() # TODO: pick a destination tile
        target_x, target_y = find_path_1step(tile) # TODO: pick a destination tile
        
        if target:
            amount = tile.units # TODO: pick amount of units to move
            actions.append('MOVE {} {} {} {} {}'.format(amount, tile.x, tile.y, target_x, target_y))

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(';'.join(actions) if len(actions) > 0 else 'WAIT')