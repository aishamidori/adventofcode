import sys
from enum import Enum

class FoldDirection(Enum):
    VERTICAL=0
    HORIZONTAL=1

def run(file_path):
    points = []
    max_x = 0
    max_y = 0
    with open(file_path) as f:

        for line in f:
            if not line.strip():
                break

            points_strs = line.strip().split(',')
            points.append((int(points_strs[1]), int(points_strs[0])))
            max_y = max(max_y, int(points_strs[0]))
            max_x = max(max_x, int(points_strs[1]))

        # HACK: This is a hack because in my input the furthest x doesn't have any
        # points in it so, my grid is smaller than the paper
        grid = generate_grid(points, (max_x + 1, max_y))
        #print_grid(grid)

        first = True
        for line in f:
            split = line.strip()[11:].split('=')
            if split[0] == 'y':
                grid = fold_horizontal(grid, int(split[1]))
            else:
                grid = fold_vertical(grid, int(split[1]))
            #print_grid(grid)

            if first:
                print('\nAfter First Fold - %d dots' % count_dots(grid))
                first = False

        print_grid(grid)

def count_dots(grid):
    count = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col]:
                count += 1
    return count

def generate_grid(points, max=(10, 10)):
    grid = [[False for _ in range(max[1] + 1)] for _ in range(max[0] + 1)]
    for point in points:
        grid[point[0]][point[1]] = True
    return grid

# Fold the bottom half up
def fold_horizontal(grid, at):
    print('\nFOLDING HORIZONTAL ON %d (old height %d)' % (at, len(grid)))
    #print_grid(grid, fold_dir=FoldDirection.HORIZONTAL, at=at)
    for col in range(len(grid[0])):
        assert grid[at][col] == False
    new_grid = [[False for _ in range(len(grid[0]))] for _ in range(at)]
    for row in range(at):
        for col in range(len(grid[0])):
            new_grid[row][col] = grid[row][col] or grid[(at * 2) - row][col]
    return new_grid

def fold_vertical(grid, at):
    print('\nFOLDING VERTICAL ON %d (old width %d)' % (at, len(grid[0])))
    #print_grid(grid, fold_dir=FoldDirection.VERTICAL, at=at)
    for row in range(len(grid)):
        assert grid[row][at] == False
    new_grid = [[False for _ in range(at)] for _ in range(len(grid))]
    for row in range(len(grid)):
        for col in range(at):
            new_grid[row][col] = grid[row][col] or grid[row][(at * 2) - col]
    return new_grid

def print_grid(grid, fold_dir=None, at=0):
    print('%d dots' % count_dots(grid))

    def get_char(row, col):
        if col == at and fold_dir == FoldDirection.VERTICAL:
            return '|'
        if row == at and fold_dir == FoldDirection.HORIZONTAL:
            return '-'
        elif grid[row][col]:
            return '#'
        else:
            return '.'

    print('\n'.join([''.join([get_char(row, col) for col in range(len(grid[0]))]) for row in range(len(grid))]))

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('Please provide a file argument')
    else:
        run(sys.argv[1])
