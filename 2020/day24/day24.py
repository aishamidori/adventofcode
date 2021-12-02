from collections import defaultdict
from copy import copy, deepcopy
from enum import IntEnum
import sys

NUM_DAYS = 100

def preprocess(file_path):
    tiles = []
    locs = defaultdict(lambda: 0)
    with open(file_path) as f:
        for line in f:
            tile = parse_dirs(line.strip())
            #print_dirs(tile)
            coords = calc_coord(tile)
            tiles.append(tile)
            locs[coords] += 1
        #print(count_black(locs))
        tile_states = get_initial_colors(locs)
        print("\nDay 0: %d" % count_black(tile_states))
        for coord in list(tile_states.keys()):
            set_empty_neighbors(coord, tile_states)
        for day in range(NUM_DAYS):
            tile_states = update_tile_states(tile_states, day+1)
            print("\nDay %d: %d" % (day+1, count_black(tile_states)))
    return tiles

def count_adjacent_black(coord, coords):
    adjacent_diffs = [
        (0,1),
        (0,-1),
        (1,0.5),
        (-1,0.5),
        (1,-0.5),
        (-1,-0.5),
    ]
    black_neighbors = 0
    for dir in adjacent_diffs:
        neighbor = (coord[0] + dir[0], coord[1] + dir[1])
        if coords[neighbor]:
            black_neighbors += 1
    return black_neighbors

def set_empty_neighbors(coord, coords):
    adjacent_diffs = [
        (0,1),
        (0,-1),
        (1,0.5),
        (-1,0.5),
        (1,-0.5),
        (-1,-0.5),
    ]
    for dir in adjacent_diffs:
        neighbor = (coord[0] + dir[0], coord[1] + dir[1])
        if not neighbor in coords:
            coords[neighbor] = False
    return coords

def update_tile_states(initial_states, day=0):
    new_states = deepcopy(initial_states)
    to_check = list(initial_states.keys())
    for coord in to_check:
        black_neighbors = count_adjacent_black(coord, initial_states)
        set_empty_neighbors(coord, new_states)
        #print(coord, "color:", 'black' if initial_states[coord] else 'white', 'neighbors:', black_neighbors)
        if initial_states[coord] and (black_neighbors == 0 or black_neighbors > 2):
            new_states[coord] = False
        elif not initial_states[coord] and (black_neighbors == 2):
            new_states[coord] = True
    return new_states

def count_black(coords):
    return sum([1 if val else 0 for val in coords.values()])


def get_initial_colors(coords):
    colors = defaultdict(lambda: False)
    for key, val in coords.items():
        # if it's odd numbered, it's black
        if val % 2 == 1:
            colors[key] = True
        else:
            colors[key] = False
    return colors

def parse_dirs(line):
    dirs = defaultdict(lambda: 0)
    i = 0
    while i < len(line):
        if line[i] in ('e', 'w'):
            dirs[line[i]] += 1
            i += 1
        else:
            dirs[line[i:i+2]] += 1
            i += 2
    return dirs

def print_dirs(tile):
    print(' '.join([' '.join([key for _ in range(tile[key])]) for key in tile]))

def calc_coord(tile):
    n = 0
    e = 0

    n += (tile['nw'] + tile['ne'])
    n -= (tile['sw'] + tile['se'])

    e += (.5 * (tile['se'] + tile['ne']))
    e -= (.5 * (tile['sw'] + tile['nw']))
    e += tile['e']
    e -= tile['w']
    return (n, e)

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        #print(part1(processed))
        #print(part2(processed))
