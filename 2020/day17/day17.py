from collections import defaultdict
import sys

def preprocess(file_path):
    initial_states = []
    with open(file_path) as f:
        for line in f:
            initial_states.append(list(line.strip()))
    return initial_states

def part1(processed):
    x_size = len(processed[0])
    y_size = len(processed)
    z_size = 1

    dimension = [processed]

    print("Starting dimension")
    print_dimension(dimension)

    for i in range(6):
        x_size += 2
        y_size += 2
        z_size += 2

        new_dimension = [empty_z_plane(x_size, y_size)]
        for plane in dimension:
            new_dimension.append(expand_plane(plane))
        new_dimension.append(empty_z_plane(x_size, y_size))

        dimension = new_dimension

        print("Before executing rules")
        print_dimension(dimension)

        dimension = execute_rules(dimension)

        print("After executing rules")
        print_dimension(dimension)

    return count_all_active(dimension)

def print_dimension(dimension):
    z = -(len(dimension) - 1) / 2
    for plane in dimension:
        print('z =', z)
        print_plane(plane)
        z += 1

def print_plane(plane):
    for row in plane:
        print(row)

def execute_rules(dimension):
    new_dimension = []
    for z in range(len(dimension)):
        new_plane = []
        for y in range(len(dimension[0])):
            new_row = []
            for x in range(len(dimension[0][0])):
                active_count = get_active_neighbors(dimension, x, y, z)
                if dimension[z][y][x] == '#':
                    if active_count in (2, 3):
                        # Remains active
                        new_row.append('#')
                    else:
                        # Becomes inactive
                        new_row.append('.')
                else:
                    if active_count == 3:
                        # Becomes active:
                        new_row.append('#')
                    else:
                        # Remains inactive
                        new_row.append('.')
            new_plane.append(new_row)
        new_dimension.append(new_plane)
    return new_dimension

def count_all_active(dimension):
    all_active = 0
    for z in range(len(dimension)):
        for y in range(len(dimension[0])):
            for x in range(len(dimension[0][0])):
                if dimension[z][y][x] == '#':
                    all_active += 1
    return all_active

def get_active_neighbors(dimension, x, y, z):
    active_neighbors = 0
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            for k in (-1, 0, 1):
                if i == j == k == 0:
                    continue
                else:
                    if is_in_range(dimension, x+k, y+j, z+i):
                        if dimension[z + i][y + j][x + k] == '#':
                            active_neighbors += 1
    return active_neighbors

def is_in_range(dimension, x, y, z):
    return ((z >= 0 and y >= 0 and x >= 0) and
        (z < len(dimension) and y < len(dimension[0]) and x < len(dimension[0][0])))

def expand_plane(plane):
    #print_plane(plane)
    empty_row = ['.' for _ in range(len(plane[0]) + 2)]
    new_plane = [empty_row]
    for row in plane:
        new_plane.append(['.'] + row + ['.'])
    new_plane.append(empty_row[:])
    #print_plane(new_plane)
    return new_plane

def empty_z_plane(x_size, y_size):
    return [['.' for _ in range(x_size)] for _ in range(y_size)]

def part2(processed):
    pass

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        print(part1(processed))
        #print(part2(processed))
