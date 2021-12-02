def print_tree(grid):
    for row in grid:
        print ' '.join(row)

inputFile = open('input.txt')

grid = []
for line in inputFile:
    grid.append(list(line))

width = len(grid[0])
height = len(grid)

print_tree(grid)

slopesToCheck = [
    (1, 1),
    (1, 3),
    (1, 5),
    (1, 7),
    (2, 1)
]

total = 1
for slope in slopesToCheck:
    row = 0
    col = 0
    treeCount = 0
    while row < height:
        if grid[row][col % (width - 1)] == '#':
            treeCount = treeCount + 1

        row = row + slope[0]
        col = col + slope[1]

    print treeCount
    total = total * treeCount

print total

