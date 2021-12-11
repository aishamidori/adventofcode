import sys
from copy import deepcopy

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        for line in f:
            processed.append([int(val) for val in line.strip()])
    return processed

def part1(processed, steps=100):
    total_flash_count = 0

    #print('BEFORE')
    #print_grid(processed, [])
    for step in range(steps):
        flashes = do_step(processed)
        #print('\nAFTER STEP %d' % step)
        #print_grid(processed, flashes)
        total_flash_count += len(flashes)
    return total_flash_count

# Flash the given coordinates and then recurse. Modifies the input (processed and flashes)
def flash(processed, row, col, flashes):
    if (row, col) in flashes:
        # Make sure we don't flash the same one twice
        return

    flashes.append((row, col))
    processed[row][col] = 0
    for deltar in range(-1, 2):
        for deltac in range(-1, 2):
            if deltar == deltac == 0 or not in_range(row + deltar, col + deltac):
                # If it's the one we're already flashing or out of range, skip
                continue
            else:
                processed[row + deltar][col + deltac] += 1
                if processed[row + deltar][col + deltac] > 9:
                    flash(processed, row + deltar, col + deltac, flashes)

def in_range(row, col):
    return (row >= 0 and row < 10 and col >= 0 and col < 10)

def do_step(processed):
    flashes = []

    # Increase all of them
    for row in range(len(processed)):
        for col in range(len(processed[0])):
            processed[row][col] += 1

    # Check for flashes (recursive)
    for row in range(len(processed)):
        for col in range(len(processed[0])):
            if processed[row][col] > 9:
                flash(processed, row, col, flashes)

    # Reset flashed coordinates to 0
    for coords in flashes:
        processed[coords[0]][coords[1]] = 0


    return flashes

def part2(processed):
    #print('BEFORE')
    #print_grid(processed, [])
    step = 0
    while True:
        flashes = do_step(processed)
        #print('\nAFTER STEP %d' % step)
        #print_grid(processed, flashes)
        step += 1

        if len(flashes) == 100:
            return step

def print_grid(processed, flashes):
    def get_display_num(row, col):
        num = processed[row][col]
        if (row, col) in flashes:
            return '\033[91m%d\033[0m' % num
        return str(num)
    print('\n')
    print('\n'.join([''.join([get_display_num(row, col) for col in range(10)]) for row in range(10)]))

if __name__ == '__main__':
    if not len(sys.argv) > 2:
        print('Please provide file and steps argument')
    else:
        processed = preprocess(sys.argv[1])

        print('----- PART 1 -----')
        # Hackily edits the input, so make a copy
        processed1 = deepcopy(processed)
        print(part1(processed1, steps=int(sys.argv[2])))

        print('----- PART 2 -----')
        print(part2(processed))
