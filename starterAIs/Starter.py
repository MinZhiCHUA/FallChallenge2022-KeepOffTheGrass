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
def optimize_recycler():
    return True

def optimize_spawn():
    return 2

def find_path():
    #find among a neutral_tiles that has the highest scrap amount
    for neutral_tile in neutral_tiles:
        highest_scrap_amount = 1
        if neutral_tile.scrap_amount > highest_scrap_amount & neutral_tile.in_range_of_recycler!=1:
            path_x = neutral_tile.x
            path_y = neutral_tile.y
    
    return path_x, path_y

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
    print("Opp_tile: ", opp_tiles,file=sys.stderr, flush=True)
    


    for tile in my_tiles:
        if tile.can_spawn:
            # Check of we should spawn here
            
            amount = optimize_spawn() # TODO: pick amount of robots to spawn here
            if amount > 0:
                actions.append('SPAWN {} {} {}'.format(amount, tile.x, tile.y))
        if tile.can_build:
            
            should_build = optimize_recycler() # TODO: pick whether to build recycler here
            if should_build:
                actions.append('BUILD {} {}'.format(tile.x, tile.y))

    for tile in my_units:
        # Find the path that has the highest scrap_amount
        target = True
        target_x, target_y = find_path() # TODO: pick a destination tile
        
        if target:
            amount = 3 # TODO: pick amount of units to move
            actions.append('MOVE {} {} {} {} {}'.format(amount, tile.x, tile.y, target_x, target_y))

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(';'.join(actions) if len(actions) > 0 else 'WAIT')