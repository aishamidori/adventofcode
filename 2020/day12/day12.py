import sys

DIRECTIONS = ['N', 'E', 'S', 'W']

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        for line in f:
            direction = line[0]
            num = line[1:]
            processed.append((direction, int(num)))
    return processed

def right(from_dir, degrees=90):
    assert degrees % 90 == 0
    index = DIRECTIONS.index(from_dir)
    return DIRECTIONS[(index + int((degrees/90))) % 4]

def left(from_dir, degrees=90):
    assert degrees % 90 == 0
    index = DIRECTIONS.index(from_dir)
    return DIRECTIONS[(index - int((degrees/90))) % 4]

def get_nsew_movement_direction(direction):
    if direction == 'N':
        return (1, 0)
    if direction == 'S':
        return (-1, 0)
    if direction == 'E':
        return (0, 1)
    if direction == 'W':
        return (0, -1)
    else:
        print('Tried to get non NSEW direction', direction)

def get_rotated_direction(original_coords, direction, num_rotations):
    new_coords = original_coords
    if direction == 'R':
        for _ in range(num_rotations):
            new_coords = (-new_coords[1], new_coords[0])
    elif direction == 'L':
        new_coords = original_coords
        for _ in range(num_rotations):
            new_coords = (new_coords[1], -new_coords[0])
    else:
        print('ERROR', direction)

    return new_coords

def xy_to_manhattan(coordinates):
    x = coordinates[0]
    y = coordinates[1]
    return abs(x) + abs(y)

def part1(processed):
    position = (0, 0)
    facing_direction = 'E'
    for (direction, distance) in processed:
        #print('\n', direction, '-', distance)
        if direction in DIRECTIONS:
            direction_tuple = get_nsew_movement_direction(direction)
            position = (position[0] + direction_tuple[0] * distance, position[1] + direction_tuple[1] * distance)
        elif direction == 'L':
            facing_direction = left(facing_direction, distance)
        elif direction == 'R':
            facing_direction = right(facing_direction, distance)
        elif direction == 'F':
            direction_tuple = get_nsew_movement_direction(facing_direction)
            position = (position[0] + direction_tuple[0] * distance, position[1] + direction_tuple[1] * distance)
        #print('Facing', facing_direction)
        #print('New Position', position)
    return xy_to_manhattan(position)

def part2(processed):
    position = (0, 0)
    waypoint = (1, 10)
    for (direction, distance) in processed:
        if direction in DIRECTIONS:
            direction_tuple = get_nsew_movement_direction(direction)
            waypoint = (waypoint[0] + direction_tuple[0] * distance, waypoint[1] + direction_tuple[1] * distance)
        elif direction in ('L', 'R'):
            waypoint = get_rotated_direction(waypoint, direction, int(distance/90))
        elif direction == 'F':
            position = (position[0] + waypoint[0] * distance, position[1] + waypoint[1] * distance)
    return xy_to_manhattan(position)

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        ##print(part1(processed))
        print(part2(processed))
