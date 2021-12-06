import sys

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        for line in f:
            coords = line.split(' -> ')
            processed.append([[int(num) for num in coord.split(',')] for coord in coords])
    return processed

def get_max(lines):
    xmax = 0
    ymax = 0
    for coords in lines:
        for coord in coords:
            xmax = max(xmax, coord[0])
            ymax = max(ymax, coord[1])
    return (xmax, ymax)

def part1(lines):
    (xmax, ymax) = get_max(lines)
    grid = [[0 for _ in range(ymax + 1)] for _ in range(xmax + 1)]

    for line in lines:
        (start, end) = line
        if start[0] == end[0]:
            for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                grid[y][start[0]] += 1
        if start[1] == end[1]:
            for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                grid[start[1]][x] += 1

    intersections = 0
    for row in grid:
        for count in row:
            if count > 1:
                intersections += 1

    return intersections

def print_grid(grid):
    print('\nCurrent Grid State:')
    for row in grid:
        print(' '.join([str(count) for count in row]))

def part2(lines):
    (xmax, ymax) = get_max(lines)
    grid = [[0 for _ in range(ymax + 1)] for _ in range(xmax + 1)]

    for line in lines:
        (start, end) = line
        if start[0] == end[0]:
            for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                grid[y][start[0]] += 1
        elif start[1] == end[1]:
            for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                grid[start[1]][x] += 1
        else:
            # Kind of messy way of getting the points in the line, since range()
            # requires a step arg to go backwards
            xrange = range(start[0], end[0] + 1)
            if start[0] > end[0]:
                xrange = range(start[0], end[0] - 1, -1)

            yrange = range(start[1], end[1] + 1)
            if start[1] > end[1]:
                yrange = range(start[1], end[1] - 1, -1)

            points = zip(xrange, yrange)
            for point in points:
                grid[point[1]][point[0]] += 1

    intersections = 0
    for row in grid:
        for count in row:
            if count > 1:
                intersections += 1

    return intersections

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])

        print('----- PART 1 -----')
        print(part1(processed))

        print('----- PART 2 -----')
        print(part2(processed))
