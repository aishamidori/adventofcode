import sys
from collections import defaultdict
from operator import attrgetter

#### GLOBAL HELPERS ####
TO_CHECK = [(1, 0), (0, 1), (-1, 0), (0, -1)]
def in_range(floor, row, col):
    return (
        (row >= 0 and row < len(floor)) and
        (col >= 0 and col < len(floor[0]))
    )

#### PART 1 ####
def preprocess(file_path):
    floor = []
    with open(file_path) as f:
        for line in f:
            floor.append([int(depth) for depth in line.strip()])
    return floor

def is_lowest_point(floor, row, col):
    point = floor[row][col]
    for (deltar, deltac) in TO_CHECK:
        if in_range(floor, row + deltar, col + deltac):
            if floor[row + deltar][col + deltac] <= point:
                return False
    return True

def part1(floor):
    #low_points = []
    total_risk = 0
    for row in range(len(floor)):
        for col in range(len(floor[0])):
            if in_range(floor, row, col) and is_lowest_point(floor, row, col):
                total_risk += 1 + floor[row][col]
                #low_points.append((row, col))

    # DEBUGGING PRINT LINES
    #def format_depth(num, is_low_point):
    #    if is_low_point:
    #        return '\033[91m%d\033[0m' % num
    #    return str(num)
    #print('\n'.join([''.join([format_depth(floor[row][col], (row, col) in low_points) for col in range(len(floor[0]))]) for row in range(len(floor))]))

    return total_risk

#### PART 2 ####
class Location:
    def __init__(self, val, coords):
        # Backpointers are larger numbers
        self.backpointers = []

        # Pointers are smaller numbers
        self.pointers = []

        self.val = val
        self.coords = coords

    @property
    def row(self):
        return self.coords[0]

    @property
    def col(self):
        return self.coords[1]

    @property
    def basin_size(self):
        counted = []
        to_check = [self]
        while to_check:
            check = to_check.pop()
            if not check in counted:
                counted.append(check)
                to_check += check.backpointers
        return len(counted)

    def __str__(self):
        # YAY PRINT DEBUGGING
        return ('''{val}
    Coordinates: ({row}, {col})
    Pointers: {pretty_pointers}
    Backpointers: {pretty_backpointers}
    Basin Size:{basin_size}''').format(
            val=self.val,
            row=self.row,
            col=self.col,
            pretty_pointers=[loc.val for loc in self.pointers],
            pretty_backpointers=[loc.val for loc in self.backpointers],
            basin_size=self.basin_size
        )

def part2(file_path):
    floor = []
    with open(file_path) as f:
        row = 0
        for line in f:
            col = 0
            row_list = []
            for depth in line.strip():
                row_list.append(Location(int(depth), (row, col)))
                col += 1

            floor.append(row_list)
            row += 1

    low_points = []

    for row in range(len(floor)):
        for col in range(len(floor[0])):
            center = floor[row][col]
            if center.val == 9:
                continue

            for (deltar, deltac) in TO_CHECK:
                if in_range(floor, row + deltar, col + deltac):
                    check = floor[row + deltar][col + deltac]
                    if check.val == 9:
                        continue

                    if check.val > center.val:
                        check.pointers.append(center)
                        center.backpointers.append(check)
                    elif check.val < center.val:
                        center.pointers.append(check)
                        check.backpointers.append(center)
            if not center.pointers:
                low_points.append(center)

    low_points.sort(key=attrgetter('basin_size'), reverse=True)
    result = 1
    for i in range(3):
        print(low_points[i])
        result *= low_points[i].basin_size

    return result

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        print('----- PART 1 -----')
        print(part1(preprocess(sys.argv[1])))

        print('----- PART 2 -----')
        print(part2(sys.argv[1]))
