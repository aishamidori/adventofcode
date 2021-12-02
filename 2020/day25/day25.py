from collections import defaultdict
from copy import copy, deepcopy

import sys

LOOP_SIZE = 8
INITIAL_SUBJECT_NUM = 7

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        for line in f:
            processed.append(int(line))
    return processed

def transform(initial_subject_number, loop_size):
    # Set the value to itself multiplied by the subject number.
    # Set the value to the remainder after dividing the value by 20201227
    value = 1
    for loop in range(loop_size):
        value *= initial_subject_number
        value %= 20201227
    return value

def find_loop_size(initial_subject_number, expected_result):
    value = 1
    loop = 1
    while True:
        value *= initial_subject_number
        value %= 20201227
        if value == expected_result:
            return loop
        loop += 1

def solve(public_keys):
    loop_1 = find_loop_size(7, public_keys[0])
    loop_2 = find_loop_size(7, public_keys[1])
    print('key:', public_keys[0], 'loop:', loop_1)
    print('key:', public_keys[1], 'loop:', loop_2)
    key1 = transform(public_keys[0], loop_2)
    key2 = transform(public_keys[1], loop_1)
    assert key1 == key2
    return key1

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        print(solve(processed))
