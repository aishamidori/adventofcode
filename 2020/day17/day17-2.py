from collections import defaultdict
import copy
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
    w_size = 1

    dimension = [[processed]]

    print("Starting dimension")
    print_dimension(dimension)

    for i in range(6):
        x_size += 2
        y_size += 2
        z_size += 2
        w_size += 2

        dimension = expand_4d(dimension, x_size, y_size, z_size)

        print("Before executing rules")
        print_dimension(dimension)

        dimension = execute_rules(dimension)

        print("After executing rules")
        print_dimension(dimension)

    return count_all_active(dimension)

def empty_3d(x_size, y_size, z_size):
    return [empty_z_plane(x_size, y_size) for _ in range(z_size)]

def expand_4d(dimension, x_size, y_size, z_size):
    new_dimension = [empty_3d(x_size, y_size, z_size)]
    for dim_3d in dimension:
        new_dimension.append(expand_3d(dim_3d, x_size, y_size))
    new_dimension.append(empty_3d(x_size, y_size, z_size))
    return new_dimension

def expand_3d(dimension, x_size, y_size):
    new_dimension = [empty_z_plane(x_size, y_size)]
    for plane in dimension:
        new_dimension.append(expand_plane(plane))
    new_dimension.append(empty_z_plane(x_size, y_size))
    return new_dimension

def expand_plane(plane):
    empty_row = ['.' for _ in range(len(plane[0]) + 2)]
    new_plane = [empty_row]
    for row in plane:
        new_plane.append(['.'] + row + ['.'])
    new_plane.append(empty_row[:])
    return new_plane

def empty_z_plane(x_size, y_size):
    return [['.' for _ in range(x_size)] for _ in range(y_size)]

def print_dimension(dimension):
    w = -(len(dimension) - 1) / 2
    for dim_3d in dimension:
        z = -(len(dimension[0]) - 1) / 2
        for plane in dim_3d:
            print('z =', z, 'w =', w)
            print_plane(plane)
            z += 1

        w += 1

def print_plane(plane):
    for row in plane:
        print(row)

def execute_rules(dimension):
    old_dimension = copy.deepcopy(dimension)
    dim_4d = []
    for w in range(len(dimension)):
        dim_3d = []
        for z in range(len(dimension[0])):
            plane = []
            for y in range(len(dimension[0][0])):
                row = []
                for x in range(len(dimension[0][0][0])):
                    active_count = get_active_neighbors(old_dimension, x, y, z, w)
                    print("(%d, %d, %d, %d)" % (w, z, y, x), "Active neighbors:", active_count)
                    if old_dimension[w][z][y][x] == '#':
                        if active_count in (2, 3):
                            # Remains active
                            print("Stays active")
                            dimension[w][z][y][x] = '#'
                            row.append('#')
                        else:
                            # Becomes inactive
                            print("Becomes inactive")
                            dimension[w][z][y][x] = '.'
                            row.append('.')
                    else:
                        if active_count == 3:
                            # Becomes active:
                            print("Becomes active")
                            dimension[w][z][y][x] = '#'
                            row.append('#')
                        else:
                            # Remains inactive
                            print("Stays inactive")
                            dimension[w][z][y][x] = '.'
                            row.append('.')
                plane.append(row)
            dim_3d.append(plane)
        dim_4d.append(dim_3d)
    return dim_4d

def count_all_active(dimension):
    all_active = 0
    for w in range(len(dimension)):
        for z in range(len(dimension[0])):
            for y in range(len(dimension[0][0])):
                for x in range(len(dimension[0][0][0])):
                    if dimension[w][z][y][x] == '#':
                        all_active += 1
    return all_active

def get_active_neighbors(dimension, x, y, z, w):
    active_neighbors = 0
    for h in (-1, 0, 1):
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                for k in (-1, 0, 1):
                    if h == i == j == k == 0:
                        continue
                    else:
                        if is_in_range(dimension, x+k, y+j, z+i, w+h):
                            #print_plane(dimension[w+h][z+i])
                            #print('IN RANGE', w+h, z+i, y+j, x+k)
                            #print('y len', len(dimension[w+h][z+i]))
                            #print('dimension[' + str(w+h) + '][' + str(z+i) + '][' + str(y+j) + ']')
                            #print('y', dimension[w + h][z + i][y + j])
                            if dimension[w + h][z + i][y + j][x + k] == '#':
                                active_neighbors += 1
    #print("W: %d Z %d Y: %d X: %d" % (w, z, y, x), "Active neighbors:", active_neighbors)
    return active_neighbors

def is_in_range(dimension, x, y, z, w):
    #print('\n', x, y, z, w)
    #print(len(dimension[0][0][0]), len(dimension[0][0]), len(dimension[0]), len(dimension))
    return ((w >= 0 and z >= 0 and y >= 0 and x >= 0) and
        (w < len(dimension) and z < len(dimension[0]) and y < len(dimension[0][0]) and x < len(dimension[0][0][0])))

def part2(processed):
    pass

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        print(part1(processed))
        #print(part2(processed))
