import sys

def preprocess(file_path):
    seat_map = []
    with open(file_path) as f:
        for line in f:
            row = list(line.strip())
            seat_map.append(row)
    return seat_map

def in_bounds(row, col, seat_map):
    rows = len(seat_map)
    cols = len(seat_map[0])
    return row >= 0 and row < rows and col >= 0 and col < cols

def get_num_occupied_adjacent(row, col, seat_map):
    adjacent_occupied = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == j == 0):
                if not in_bounds(row + i, col + j, seat_map):
                    continue

                if seat_map[row + i][col + j] == '#':
                    adjacent_occupied += 1

    return adjacent_occupied

def part1(seat_map):
    old_map = None
    new_map = seat_map
    it = 1
    while old_map != new_map:
        #print('Iteration', it)
        it += 1

        old_map = new_map
        #print("BEFORE")
        #print_map(old_map)
        new_map = get_new_seat_map_part_1(new_map)
        #print("AFTER")
        #print_map(new_map)

    print(count_occupied(new_map))

def count_occupied(seat_map):
    tot_occ = 0
    for row in seat_map:
        for seat in row:
            if seat == '#':
                tot_occ += 1
    return tot_occ

def print_map(seat_map):
    for row in seat_map:
        print(''.join(row))

def get_new_seat_map_part_1(seat_map):
    new_seat_map = []
    for row in range(len(seat_map)):
        new_row = []
        for col in range(len(seat_map[0])):
            curr = seat_map[row][col]

            # Empty
            if curr == '.':
                new_row.append(curr)
                continue

            adjacent_occupied = get_num_occupied_adjacent(row, col, seat_map)

            # Rule 1: Empty with no occupied adjacent seats
            if curr == 'L' and adjacent_occupied == 0:
                new_row.append('#')
            # Rule 2: Occupied with too many adjacent seats
            elif curr == '#' and adjacent_occupied >= 4:
                new_row.append('L')
            # Doesn't match a rule
            else:
                new_row.append(curr)
        new_seat_map.append(new_row)

    return new_seat_map

def part2(seat_map):
    old_map = None
    new_map = seat_map
    it = 1

    #print("BEFORE")
    #print_map(new_map)
    while old_map != new_map:
        it += 1
        old_map = new_map
        new_map = get_new_seat_map_part_2(new_map)

        #print('\nIteration', it)
        #print_map(new_map)

    print(count_occupied(new_map))

def get_new_seat_map_part_2(seat_map):
    new_seat_map = []
    for row in range(len(seat_map)):
        new_row = []
        for col in range(len(seat_map[0])):
            curr = seat_map[row][col]

            # Empty
            if curr == '.':
                new_row.append(curr)
                continue

            adjacent_occupied = get_num_visible(row, col, seat_map)

            # Rule 1: Empty with no occupied adjacent seats
            if curr == 'L' and adjacent_occupied == 0:
                new_row.append('#')
            # Rule 2: Occupied with too many adjacent seats
            elif curr == '#' and adjacent_occupied >= 5:
                new_row.append('L')
            # Doesn't match a rule
            else:
                new_row.append(curr)
        new_seat_map.append(new_row)

    return new_seat_map


def get_num_visible(row, col, seat_map):
    visible = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == j == 0):
                continue

            new_row = row + i
            new_col = col + j
            while in_bounds(new_row, new_col, seat_map):
                if seat_map[new_row][new_col] == '#':
                    visible += 1
                    break

                if seat_map[new_row][new_col] == 'L':
                    break

                new_row += i
                new_col += j

    return visible

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        #print(part1(processed))
        print(part2(processed))
