import sys
from collections import defaultdict

def preprocess(file_path):
    fish = defaultdict(lambda: 0)
    with open(file_path) as f:
        input = f.readline().strip()
        for num in input.split(','):
            fish[int(num)] += 1

    return fish

def solve(start, days):
    fish = start.copy()
    for _ in range(days):
        fish_copy = fish.copy()
        for days, count in fish.items():
            if days == 0:

                # Create new fish
                fish_copy[8] += count

                # Reset these fish timers
                fish_copy[days] -= count
                fish_copy[6] += count

            else:
                fish_copy[days] -= count
                fish_copy[days - 1] += count
        fish = fish_copy

    return sum(fish.values())

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('Please provide a file argument')
    else:
        processed = preprocess(sys.argv[1])

        print('----- PART 1 -----')
        print(solve(processed, 80))

        print('----- PART 2 -----')
        print(solve(processed, 256))
