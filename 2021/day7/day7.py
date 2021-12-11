import math
import sys

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        processed = [int(num) for num in f.readline().strip().split(',')]
    return processed

def part1(processed):
    processed.sort()
    target = processed[round(len(processed)/2)]
    return sum(list(map(lambda pos: abs(pos-target), processed)))

def part2(processed):
    processed.sort()
    avg = sum(processed) / len(processed)
    targets = [math.floor(avg), math.ceil(avg)]
    return min(list(map(lambda target: sum(list(map(lambda pos: sum(range(abs(pos - target) + 1)), processed))), targets)))

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('Please provide a file argument')
    else:
        processed = preprocess(sys.argv[1])

        print('----- PART 1 -----')
        print(part1(processed))

        print('----- PART 2 -----')
        print(part2(processed))
