from collections import defaultdict
import sys

tile_blocks = {}

def preprocess(file_path):
    tiles = {}
    with open(file_path) as f:
        while True:
            #print("New tile")
            header = f.readline().strip()
            if not header:
                break

            #print(header)
            tile_num = header.split(' ')[1].strip(":")
            #print(tile_num)
            tile = []
            for line in f:
                print(line)
                if line == '\n':
                    # Finished the tile
                    break
                else:
                    tile.append(list(line.strip()))
            #print_tile(tile_num, tile)
            tiles[int(tile_num)] = get_edges(tile)
            global tile_blocks
            tile_blocks[int(tile_num)] = tile
    return tiles

def part1(tiles):
    edge_dict = defaultdict(set)
    for tile_n, edges in tiles.items():
        for edge in edges.values():
            edge_dict[''.join(edge)].add(tile_n)

    prod = 1

    for tile_n, edges in tiles.items():
        print('\n TILE', tile_n)
        print_tile(tile_n, tile_blocks[tile_n])

        # Matches for top
        top = edges['top']
        top_str = ''.join(top)
        top_match = edge_dict[top_str].union(edge_dict[top_str[::-1]])
        top_match.remove(tile_n)
        print("top of", tile_n, 'matches tile', top_match, '[%s]' % top_str)
        if top_match:
            neighbor = top_match.pop()
            top_match.add(neighbor)
            print_tile(neighbor, tile_blocks[neighbor])


        right = edges['right']
        right_str = ''.join(right)
        right_match = edge_dict[right_str].union(edge_dict[right_str[::-1]])
        right_match.remove(tile_n)
        print("right of", tile_n, 'matches tile', right_match, '[%s]' % right_str)
        if right_match:
            neighbor = right_match.pop()
            right_match.add(neighbor)
            print_tile(neighbor, tile_blocks[neighbor])

        bottom = edges['bottom']
        bottom_str = ''.join(bottom)
        bottom_match = edge_dict[bottom_str].union(edge_dict[bottom_str[::-1]])
        bottom_match.remove(tile_n)
        print("bottom of", tile_n, 'matches tile', bottom_match, '[%s]' % bottom_str)
        if bottom_match:
            neighbor = bottom_match.pop()
            bottom_match.add(neighbor)
            print_tile(neighbor, tile_blocks[neighbor])

        left = edges['left']
        left_str = ''.join(left)
        left_match = edge_dict[left_str].union(edge_dict[left_str[::-1]])
        left_match.remove(tile_n)
        print("left of", tile_n, 'matches tile', left_match, '[%s]' % left_str)
        if left_match:
            neighbor = left_match.pop()
            left_match.add(neighbor)
            print_tile(neighbor, tile_blocks[neighbor])

        if len(top_match.union(right_match).union(bottom_match).union(left_match)) == 2:
            print("Tile", tile_n, "is a corner")
            prod *= tile_n

        print('Neighbors of', tile_n, '-', top_match.union(right_match).union(bottom_match).union(left_match))

    return prod

def rotate_or_flip_to_match(to_move, to_match):
    pass


def print_tile(num, tile):
    print("Tile", num)
    for row in tile:
        print("".join(row))

def get_edges(tile_data):
    return {
        'top': tile_data[0],
        'right': [row[-1] for row in tile_data],
        'left': [row[0] for row in tile_data],
        'bottom': tile_data[-1]
    }

def flip_horiz(edges):
    return {
        'top': edges['top'][::-1],
        'right': edges['left'],
        'left': edges['right'],
        'bottom': edges['bottom'][::-1]
    }

def flip_vert(edges):
    return {
        'top': edges['bottom'],
        'right': edges['left'][::-1],
        'left': edges['right'][::-1],
        'bottom': edges['top']
    }

def rotate_counter(edges):
    return {
        'top': edges['left'][::-1],
        'right': edges['top'],
        'left': edges['bottom'],
        'bottom': edges['right'][::-1]
    }

def rotate_clockwise(edges):
    return {
        'top': edges['right'],
        'right': edges['bottom'][::-1],
        'left': edges['top'][::-1],
        'bottom': edges['left']
    }


class Tile:
    def __init__(data):
        self.data = data
        self.edges = get_edges(data)

    @property
    def edges():
        return get_edges(self.data)


    def rotate():
        new_data = []
        for i in range(len(data)):


def part2(tiles):
    edge_dict = defaultdict(set)
    for tile_n, edges in tiles.items():
        for edge in edges.values():
            edge_dict[''.join(edge)].add(tile_n)

    tile_neighbor_dict = {}
    corners = []
    for tile_n, edges in tiles.items():
        # Matches for top
        top = edges['top']
        top_str = ''.join(top)
        top_match = edge_dict[top_str].union(edge_dict[top_str[::-1]])
        top_match.remove(tile_n)
        #print("top of", tile_n, 'matches tile', top_match)

        right = edges['right']
        right_str = ''.join(right)
        right_match = edge_dict[right_str].union(edge_dict[right_str[::-1]])
        right_match.remove(tile_n)
        #print("right of", tile_n, 'matches tile', right_match)

        bottom = edges['bottom']
        bottom_str = ''.join(bottom)
        bottom_match = edge_dict[bottom_str].union(edge_dict[bottom_str[::-1]])
        bottom_match.remove(tile_n)
        #print("bottom of", tile_n, 'matches tile', bottom_match)

        left = edges['left']
        left_str = ''.join(left)
        left_match = edge_dict[left_str].union(edge_dict[left_str[::-1]])
        left_match.remove(tile_n)
        #print("left of", tile_n, 'matches tile', left_match)

        tile_neighbors = {}
        if top_match:
            tile_neighbors['top'] = top_match.pop()
        if right_match:
            tile_neighbors['right'] = right_match.pop()
        if bottom_match:
            tile_neighbors['bottom'] = bottom_match.pop()
        if left_match:
            tile_neighbors['left'] = left_match.pop()

        tile_neighbor_dict[tile_n] = tile_neighbors
        if len(tile_neighbors.values()) == 2:
            print("Tile", tile_n, "is a corner")
            corners.append(tile_n)

    unplaced = set(tiles.keys())
    tile = corners[0]

    full_grid = []
    row = [tile]
    # Rotate the first corner
    while tile_neighbor_dict[tile]['left'] or tile_neighbor_dict[tile]['top']:
        tile_neighbor_dict[tile] = rotate_neighbors(tile_neighbor_dict[tile])
        edge_dict[tile] = rotate_clockwise(edge_dict[tile])

    while True:
        right_edge = tiles[tile]['right']
        if right_edge in edge_dict:
            break

def rotate_neighbors(neighbors):
    return {
        'top': neighbors['left'],
        'right': neighbors['top'],
        'left': neighbors['bottom'],
        'bottom': neighbors['right']
    }

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        #print(part1(processed))
        print(part2(processed))
