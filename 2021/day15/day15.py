import sys
from heapq import heappop, heappush
from math import floor

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        for line in f:
            processed.append([int(level) for level in line.strip()])
    return processed

def solve(input_grid, scale=1):
    path_risks = [[sys.maxsize for _ in range(len(input_grid[0]) * scale)] for _ in range(len(input_grid) * scale)]
    path_risks[0][0] = input_grid[0][0]

    path_dirs = [[None for _ in range(len(input_grid[0]) * scale)] for _ in range(len(input_grid) * scale)]
    visited = [[False for _ in range(len(input_grid[0]) * scale)] for _ in range(len(input_grid) * scale)]

    queue = []

    # Tuples in the format (priority, coords)
    heappush(queue, (0, (0, 0)))
    while queue:
        path_cost, current = heappop(queue)
        if visited[current[0]][current[1]]:
            continue

        visited[current[0]][current[1]] = True
        for delta in [(0, 1), (1, 0), (0, -1), (-1, 0)]:

            nextr, nextc = current[0] + delta[0], current[1] + delta[1]
            if in_range(path_risks, nextr, nextc) and not visited[nextr][nextc]:
                maybe_min = path_cost + get_loc_cost(input_grid, nextr, nextc)
                if maybe_min < path_risks[nextr][nextc]:
                    path_dirs[nextr][nextc] = (-1 * delta[0], -1 * delta[1])
                    path_risks[nextr][nextc] = maybe_min
                heappush(queue, (path_risks[nextr][nextc], (nextr, nextc)))

    print_dirs(path_dirs)
    return path_risks[-1][-1]

def in_range(grid, row, col):
    return row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0])

def get_loc_cost(loc_risks, row, col):
    cost = (
        loc_risks[row % len(loc_risks)][col % len(loc_risks[0])] +
        max(0, floor(row / len(loc_risks)) + floor(col / len(loc_risks[0])))
    )
    return (cost % 9) if cost > 9 else cost

def print_dirs(dirs):
    grid_path = []
    grid_path.append((len(dirs) - 1, len(dirs[0]) - 1))
    while grid_path[-1][0] > 0 or grid_path[-1][1] > 0:
        direction = dirs[grid_path[-1][0]][grid_path[-1][1]]
        curr = (grid_path[-1][0] + direction[0], grid_path[-1][1] + direction[1])
        grid_path.append(curr)

    def get_display(coords):
        if coords in grid_path:
            return '\033[91m%d\033[0m' % get_loc_cost(coords[0], coords[1])
        else:
            return str(get_loc_cost(coords[0], coords[1]))

    print('\n'.join([''.join([get_display((row, col)) for col in range(len(dirs[0]))]) for row in range(len(dirs))]))

def print_grid(risks):
    def get_display(risk):
        if risk in (None, sys.maxsize):
            return '-'
        else:
            return str(risk)

    print('\n'.join(['\t'.join([get_display(risks[row][col]) for col in range(len(risks[0]))]) for row in range(len(risks))]))

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('Please provide a file argument')
    else:
        processed = preprocess(sys.argv[1])

        print('----- PART 1 -----')
        print(solve(processed))

        print('----- PART 2 -----')
        print(solve(processed, scale=5))
