import sys

def part1(ranges):
    velocities = []
    x_range, y_range = ranges
    max_num = 0
    for x_vel in range(200):
        for y_vel in range(-150, 150):
            positions = get_positions((x_vel, y_vel), 300)
            num = 0
            for pos in positions:
                if in_range(pos, x_range, y_range):
                    max_num = max(max_num, num)
                    velocities.append((x_vel, y_vel))
                num += 1

    return velocities

def in_range(point, x_range, y_range):
    #print('checking %s in range x=%s, y=%s (%s and %s)' % (str(point), str(x_range), str(y_range), point[0] in range(x_range[0], x_range[1] + 1), point[1] in range(y_range[0], y_range[1] + 1)))
    return point[0] in range(x_range[0], x_range[1] + 1) and point[1] in range(y_range[0], y_range[1] + 1)

def draw_path(velocity, target_range):
    target_x_range, target_y_range = target_range
    positions = get_positions(velocity, 40)

    # Only render the ones until the range
    filtered_pos = []
    for pos in positions:
        #print(pos)
        filtered_pos.append(pos)
        if in_range(pos, target_x_range, target_y_range):
            break

    #print(positions)
    grid_x_range = (
        min(target_x_range[0], *[pos[0] for pos in filtered_pos]) - 1,
        max(target_x_range[1], *[pos[0] for pos in filtered_pos]) + 1
    )
    grid_y_range = (
        min(target_y_range[0], *[pos[1] for pos in filtered_pos]) - 1,
        max(target_y_range[1], *[pos[1] for pos in filtered_pos]) + 1
    )
    grid = [[' ' for _ in range(grid_x_range[1] - grid_x_range[0])] for _ in range(grid_y_range[1] - grid_y_range[0])]
    for x in range(target_x_range[0] - grid_x_range[0], target_x_range[1] - grid_x_range[0] + 1):
        for y in range(target_y_range[0] - grid_y_range[0], target_y_range[1] - grid_y_range[0] + 1):
            grid[y][x] = 'T'

    for pos in filtered_pos:
        grid[pos[1] - grid_y_range[0]][pos[0] - grid_x_range[0]] = '#'

    grid[0 - grid_y_range[0]][0 - grid_x_range[0]] == 'S'

    print('\n'.join([''.join([grid[y][x] for x in range(len(grid[0]))]) for y in range(len(grid) - 1, -1, -1)]))

def get_positions(velocity, steps):
    positions = [(0, 0)]
    x_vel, y_vel = velocity
    for step in range(steps):
        positions.append((positions[-1][0] + x_vel, positions[-1][1] + y_vel))
        if x_vel > 0:
            x_vel -= 1
        elif x_vel < 0:
            x_vel += 1
        y_vel -= 1
    return positions

def part2(processed):
    pass

def preprocess(file_path):
    # Example: target area: x=124..174, y=-123..-86
    with open(file_path) as f:
        line = f.readline().strip()
        coords = line[13:].split(', ')
        x_range = [int(num) for num in coords[0][2:].split('..')]
        y_range = [int(num) for num in coords[1][2:].split('..')]
    return (x_range, y_range)

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        #draw_path((7,2), ((20,30),(-10,-5)))
        with open('test-output.txt') as f:
            x_range = [20,30]
            y_range = [-10,-5]
            expected_velocities = []
            for line in f:
                if line:
                    expected_velocities.append(tuple([int(num) for num in line.strip().split(',')]))

            draw_path((27,-5), (x_range, y_range))
            draw_path((9,0), (x_range, y_range))

            actual_velocities = part1((x_range, y_range))

            for velocity in expected_velocities:
                if velocity not in actual_velocities:
                    print("missing", velocity)

            for velocity in actual_velocities:
                if velocity not in expected_velocities:
                    print("incorrect", velocity)

            print("Correct Count:", len(expected_velocities))
            print("Calculated Count:", len(actual_velocities))
            print("Calculated Count (set):", len(set(actual_velocities)))
    else:
        ranges = preprocess(sys.argv[1])

        print('----- PART 1 -----')
        print(len(set(part1(ranges))))

        print('----- PART 2 -----')
        print(part2(ranges))
