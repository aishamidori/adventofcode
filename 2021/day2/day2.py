from collections import defaultdict
from copy import copy, deepcopy

import sys

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        for line in f:
            split = line.split(' ')
            processed.append((split[0], int(split[1])))
    return processed

def part1(processed):
    pos = 0
    depth = 0
    for (op, dist) in processed:
        print(op, dist)
        if op == 'up':
            depth -= dist
        elif op == 'down':
            depth += dist
        elif op == 'forward':
            pos += dist

    print('Horizontal Position -', pos)
    print('Depth -', depth)

    return pos * depth

def part2(processed):
    pos = 0
    depth = 0
    aim = 0
    for (op, dist) in processed:
        print(op, dist)
        if op == 'up':
            aim -= dist
        elif op == 'down':
            aim += dist
        elif op == 'forward':
            pos += dist
            depth += aim * dist

    print('Horizontal Position -', pos)
    print('Depth -', depth)

    return pos * depth

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        #print(part1(processed))
        print(part2(processed))
