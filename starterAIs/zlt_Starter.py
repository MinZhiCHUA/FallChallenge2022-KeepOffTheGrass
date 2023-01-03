import sys
import random
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
    return random.randint(0, 1)

def optimize_spawn():
    return random.randint(1, 3)

def find_target():
    #find among a neutral_tiles that has the highest scrap amount
    highest_scrap_amount = 1
    target = opp_tiles[0]
    for opp_tile in opp_tiles:
        if opp_tile.scrap_amount > highest_scrap_amount & opp_tile.in_range_of_recycler != 1:
            target = opp_tile
            highest_scrap_amount = opp_tile.scrap_amount
    return target

def euclidean_distance(a_x,a_y,b_x,b_y):
    return ((a_x-b_x)**2 + (a_y-b_y)**2)**0.5

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
        target = find_target()
        
        if target:
            amount = tile.units # TODO: pick amount of units to move
            actions.append('MOVE {} {} {} {} {}'.format(amount, tile.x, tile.y, target.x, target.y))

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(';'.join(actions) if len(actions) > 0 else 'WAIT')