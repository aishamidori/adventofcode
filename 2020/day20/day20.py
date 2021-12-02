from collections import defaultdict
from copy import copy, deepcopy
from enum import Enum
import math
import sys

class Side(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    TOP = 'top'
    BOTTOM = 'bottom'

    @staticmethod
    def sides():
        return [side.value for side in Side]

class Tile:
    def __init__(self, num, data):
        self.num = num
        self.data = data
        self.neighbors = {
            Side.LEFT: None,
            Side.RIGHT: None,
            Side.TOP: None,
            Side.BOTTOM: None
        }
        self.neighbor_set = set()
        self.flipped = False
        self.rotations = 0
        self.final_pos = None

    @property
    def top(self):
        return ''.join(self.data[0])

    @property
    def bottom(self):
        return ''.join(self.data[-1])

    @property
    def left(self):
        return ''.join([row[0] for row in self.data])

    @property
    def right(self):
        return ''.join([row[-1] for row in self.data])

    @property
    def edges(self):
        return {
            Side.TOP: self.top,
            Side.BOTTOM: self.bottom,
            Side.LEFT: self.left,
            Side.RIGHT: self.right
        }

    def is_edge(self):
        return len(self.neighbor_set) == 3

    def is_corner(self):
        return len(self.neighbor_set) == 2

    def add_neighbor(self, new_neighbor, side='top'):
        if new_neighbor == self:
            return


        assert side in Side
        self.neighbors[side] = new_neighbor
        self.neighbor_set.add(new_neighbor)

    def rotate(self):
        new_data = []
        for i in range(len(self.data)):
            row = []
            for j in range(len(self.data) - 1, -1, -1):
                row.append(self.data[j][i])
            new_data.append(row)
        self.data = new_data
        self.rotations = (self.rotations + 1) % 4

        self.neighbors = {
            Side.TOP: self.neighbors[Side.LEFT],
            Side.BOTTOM: self.neighbors[Side.RIGHT],
            Side.LEFT: self.neighbors[Side.BOTTOM],
            Side.RIGHT: self.neighbors[Side.TOP]
        }

    def flip(self):
        new_data = []
        for i in range(len(self.data) - 1, -1, -1):
            new_data.append(self.data[i])
        self.data = new_data
        self.flipped = not self.flipped
        bottom_neighbor = self.neighbors[Side.BOTTOM]
        top_neighbor = self.neighbors[Side.TOP]
        self.neighbors[Side.BOTTOM] = top_neighbor
        self.neighbors[Side.TOP] = bottom_neighbor

    def __str__(self):
        return """Tile {num} {final_pos}
{tile_data}
Neighbors: {neighbors}
Rotations: {rotations}
Flipped: {flipped}
""".format(
    num=self.num,
    final_pos=self.final_pos,
    tile_data='\n'.join([''.join(row) for row in self.data]),
    neighbors={tile.num for tile in self.neighbor_set},
    rotations=self.rotations,
    flipped=self.flipped

)

class Image:
    def __init__(self, data, with_borders=None):
        self.data = data
        self.with_borders =  with_borders
        self.flipped = False
        self.rotations = 0

    def rotate(self):
        new_data = []
        for i in range(len(self.data)):
            row = []
            for j in range(len(self.data) - 1, -1, -1):
                row.append(self.data[j][i])
            new_data.append(row)
        self.data = new_data
        self.rotations = (self.rotations + 1) % 4

    def flip(self):
        new_data = []
        for i in range(len(self.data) - 1, -1, -1):
            new_data.append(self.data[i])
        self.data = new_data
        self.flipped = not self.flipped

    def is_in_bounds(self, row, col):
        return ((row >= 0 and row < len(self.data)) and
                    (col >= 0 and col < len(self.data[0])))

    def find_seamonsters(self, seamonster):
        num_monsters = 0
        data_copy = deepcopy(self.data)
        for r1 in range(len(self.data)):
            for c1 in range(len(self.data[0])):
                #print("Searching at (%d, %d)" % (r1, c1))
                found = True
                for r2 in range(len(seamonster)):
                    for c2 in range(len(seamonster[0])):
                        if seamonster[r2][c2] == '#':
                            if self.is_in_bounds(r1 + r2, c1 + c2) and self.data[r1 + r2][c1 + c2] == '#':
                                #print("(%d, %d) - %s [Still Matches]" % (r1+r2, c1+c2, self.data[r1 + r2][c1 + c2]))
                                continue
                            else:
                                #print("No seamonster at (%d, %d)" % (r1, c1))
                                found = False
                                break
                    if found == False:
                        break

                # Found a full sea monster
                if found == True:
                    print("Found a seamonster at (%d, %d)" % (r1, c1))
                    num_monsters += 1
                    for r2 in range(len(seamonster)):
                        for c2 in range(len(seamonster[0])):
                            if seamonster[r2][c2] == '#':
                                data_copy[r1+r2][c1+c2] = 'O'

        if num_monsters > 0:
            print('\n'.join([''.join(row) for row in data_copy]))
            num_nonmonster_pound = 0
            for r in range(len(self.data)):
                for c in range(len(self.data[0])):
                    if data_copy[r][c] == '#':
                        num_nonmonster_pound += 1
            print("Number of non-monster #s:", num_nonmonster_pound)

        return num_monsters

    def __str__(self):
        return """Final Image:
{tile_data}
Rotations: {rotations}
Flipped: {flipped}
""".format(
        tile_data='\n'.join([''.join(row) for row in self.with_borders]),
        rotations=self.rotations,
        flipped=self.flipped
    )

all_tiles = {}
edge_map = defaultdict(set)
corners = []
final_map = []

def part2(seamonster):
    image = make_image()
    return search_for_seamonster(image, seamonster)

def search_for_seamonster(image, seamonster):
    seamonster_count = 0
    for i in range(4):
        seamonsters = image.find_seamonsters(seamonster)
        seamonster_count += seamonsters
        #print(image)
        print('Rotation %d -' % i, seamonsters, 'seamonsters')
        image.rotate()

    image.flip()

    for i in range(4):
        seamonsters = image.find_seamonsters(seamonster)
        seamonster_count += seamonsters
        #print(image)
        print('Rotation %d -' % i, seamonsters, 'seamonsters')
        image.rotate()
    return seamonster_count

def make_image():
    global all_tiles
    global edge_map
    global corners
    global final_map

    TILE_SIDE_LEN = int(math.sqrt(len(all_tiles.values())))
    IMG_SIDE_LEN = TILE_SIDE_LEN * 8

    placed = set()
    final_map = [[None for _ in range(TILE_SIDE_LEN)] for _ in range(TILE_SIDE_LEN)]

    first_tile = corners[0]
    rotate_to_fit(first_tile, (0, 0))
    final_map[0][0] = first_tile
    first_tile.final_pos = (0, 0)

    #print(first_tile)

    last_coords = (0, 0)
    while last_coords != (TILE_SIDE_LEN - 1, TILE_SIDE_LEN - 1):
        next_coords = (last_coords[0], last_coords[1] + 1)
        next_tile = None

        # Next tile to the right
        if is_in_bounds_tile(*next_coords):
            #print('last', last_coords)
            #print('next', next_coords)

            # Get next tile
            last_tile = final_map[last_coords[0]][last_coords[1]]
            next_tile = last_tile.neighbors[Side.RIGHT]
            #print(next_tile)

        # Hit the end of a row
        else:
            last_coords = (last_coords[0], 0)
            next_coords = (last_coords[0] + 1, 0)

            #print('last', last_coords)
            #print('next', next_coords)

            last_tile = final_map[last_coords[0]][last_coords[1]]
            next_tile = last_tile.neighbors[Side.BOTTOM]
            #print(next_tile)

        # Place and position
        rotate_to_fit(next_tile, next_coords)
        final_map[next_coords[0]][next_coords[1]] = next_tile
        next_tile.final_pos = next_coords
        #print_full_map()

        # Continue
        last_coords = next_coords

    image = Image(generate_full_image(), with_borders=generate_full_image_with_borders())
    print(image)
    return image

def print_full_map():
    print("\nFULL MAP")
    for row in final_map:
        nums = []
        for tile in row:
            if tile != None:
                nums.append(str(tile.num))
            else:
                nums.append('_')
        print(' '.join(nums))

def generate_full_image():
    image = [['_' for _ in range(len(final_map[0]) * 8)] for _ in range(len(final_map) * 8)]
    for r in range(len(final_map)):
        for c in range(len(final_map[0])):
            tile = final_map[r][c]
            if not tile:
                continue
            for r2 in range(len(tile.data[0]) - 2):
                for c2 in range(len(tile.data) - 2):
                    row = 8 * r + r2
                    col = 8 * c + c2
                    image[row][col] = tile.data[r2 + 1][c2 + 1]
    return image

def generate_full_image_with_borders():
    image = [[' ' for _ in range(len(final_map[0]) * 11)] for _ in range(len(final_map) * 11)]
    for r in range(len(final_map)):
        for c in range(len(final_map[0])):
            tile = final_map[r][c]
            if not tile:
                continue
            for r2 in range(len(tile.data[0])):
                row = 11 * r + r2
                for c2 in range(len(tile.data)):

                    col = 11 * c + c2
                    image[row][col] = tile.data[r2][c2]
    return image

def is_in_bounds_tile(row, col):
    global final_map

    return ((row >= 0 and row < len(final_map)) and
        (col >= 0 and col < len(final_map[0])))

def rotate_to_fit(tile, loc):
    #print("Rotating/flipping tile", tile.num)
    global final_map
    global edge_map

    row, col = loc
    top = (row - 1, col)
    bottom = (row + 1, col)
    left = (row, col - 1)
    right = (row, col + 1)

    match_lambdas = []
    if is_in_bounds_tile(*top):
        top_tile = final_map[top[0]][top[1]]
        if top_tile:
            #print("Rotating to match top tile", top_tile.bottom)
            match_lambdas.append(lambda: top_tile.bottom == tile.top)
    else:
        #print("Rotating to match top edge")
        match_lambdas.append(lambda: not tile.neighbors[Side.TOP])

    if is_in_bounds_tile(*bottom):
        bottom_tile = final_map[bottom[0]][bottom[1]]
        if bottom_tile:
            #print("Rotating to match bottom tile")
            match_lambdas.append(lambda: bottom_tile.top == tile.bottom)
    else:
        #print("Rotating to match bottom edge")
        match_lambdas.append(lambda: not tile.neighbors[Side.BOTTOM])

    if is_in_bounds_tile(*left):
        left_tile = final_map[left[0]][left[1]]
        if left_tile:
            #print("Rotating to match left tile")
            match_lambdas.append(lambda: left_tile.right == tile.left)
    else:
        #print("Rotating to match left edge")
        match_lambdas.append(lambda: not tile.neighbors[Side.LEFT])

    if is_in_bounds_tile(*right):
        right_tile = final_map[right[0]][right[1]]
        if right_tile:
            #print("Rotating to match right tile")
            match_lambdas.append(lambda: right_tile.left == tile.right)
    else:
        #print("Rotating to match right edge")
        match_lambdas.append(lambda: not tile.neighbors[Side.RIGHT])

    rotations = 0
    flipped = False
    while not all(match_lambda() for match_lambda in match_lambdas):
        #print(match_lambdas)
        #print("Not matching yet neighbors:", tile.neighbors)
        if rotations <= 4:
            #print("Rotating")
            tile.rotate()
            rotations += 1
        elif flipped == False:
            #print("Flipping")
            tile.flip()
            flipped = True
            rotations = 0
        else:
            print("Unable to find a match")
            break

def test_tile_funcs(tiles):
    example_tile = list(tiles.values())[0]
    print_tile(example_tile)

    print("FLIPPING HORIZONTAL")
    example_tile.flip_horizontal()
    print_tile(example_tile)

    print("FLIPPING VERTICAL")
    example_tile.flip_vertical()
    print_tile(example_tile)

    print("ROTATING")
    example_tile.rotate()
    print_tile(example_tile)

def preprocess(file_path):
    global all_tiles
    global edge_map
    global corners

    with open(file_path) as f:
        while True:
            header = f.readline().strip()
            if not header:
                break

            tile_num = header.split(' ')[1].strip(":")
            tile_data = []
            for line in f:
                if line == '\n':
                    # Finished the tile
                    break
                else:
                    tile_data.append(list(line.strip()))

            tile = Tile(int(tile_num), tile_data)
            all_tiles[int(tile_num)] = tile
            for edge in tile.edges.values():
                edge_map[edge].add(tile)
                edge_map[edge[::-1]].add(tile)

    for tile in all_tiles.values():
        for (side, edge) in tile.edges.items():
            for neighbor in edge_map[edge]:
                tile.add_neighbor(neighbor, side=side)
        if tile.is_corner():
            corners.append(tile)

def read_sea_monster_pattern(file_path):
    sea_monster = []
    with open(file_path) as f:
        for line in f:
            sea_monster.append(list(line))
    print('\n'.join([str(row) for row in sea_monster]))
    return sea_monster

if __name__ == "__main__":
    if not len(sys.argv) > 2:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        sea_monster = read_sea_monster_pattern(sys.argv[2])
        print(part2(sea_monster))
