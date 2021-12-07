import sys

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        processed = [int(num) for num in f.readline().strip().split(',')]
    return processed

def part1(processed):
    processed.sort()
    return find_min_fuel(processed, lambda pos, target: abs(pos-target))

def part2(processed):
    processed.sort()
    return find_min_fuel(processed, lambda pos, target: sum(range(abs(pos - target) + 1)))

def find_min_fuel(sorted, calc_func):
    min_fuel = None
    for target in range(sorted[-1] + 1):
        fuel = 0
        for pos in processed:
            fuel += calc_func(pos, target)

        # Update min if necessary
        if not min_fuel or fuel < min_fuel:
            min_fuel = fuel
        else:
            # Once it starts going up again, we're done!
            break

    return min_fuel


if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])

        print('----- PART 1 -----')
        print(part1(processed))

        print('----- PART 2 -----')
        print(part2(processed))
