import sys
from bitarray import bitarray, util


def preprocess(file_path):
    """
    Parses the input file into a list of bitarrays.
    Expected file contents: one number per line in base 2.
    """
    processed = []
    with open(file_path) as f:
        for line in f:
            processed.append(bitarray(line.strip()))
    return processed

def part1(processed):
    """
    Given a list of bitarrays, calculates the "gamma rate" and "epsilon rate",
    which consist of the most common bits and least common bits at each index
    respectively.

    Returns the product of gamma * epsilon rates.
    """
    gamma = bitarray()
    for index in range(len(processed[0])):
        gamma.append(most_frequent_bit(processed, index))

    epsilon = ~gamma
    return util.ba2int(gamma) * util.ba2int(epsilon)

def part2(processed):
    """
    Given a list of bitarrays, calculates the "oxygen generator rating" and
    "CO2 scrubber rating". For each, the numbers are filtered at each subsequent
    index for the most common bit (oxygen generator) and least common bit (c02
    scrubber).

    Returns the product of oxygen generator * CO2 srubber rates.
    """
    o2 = filter_nums(processed, lambda nums, index: most_frequent_bit(nums, index))
    co2 = filter_nums(processed, lambda nums, index: 1 - most_frequent_bit(nums, index))

    return util.ba2int(o2) * util.ba2int(co2)


def filter_nums(nums, get_bit_to_keep):
    """
    Given a list of numbers (represented as bitarrays) and a function which
    calculates which bit we want to keep at each step, filter the list bit by
    bit.
    """
    nums_copy = nums[:]

    index = 0
    while len(nums_copy) > 1:
        to_match = get_bit_to_keep(nums_copy, index)
        nums_copy = [num for num in nums_copy if num[index] == to_match]
        index += 1

    return nums_copy[0]

def most_frequent_bit(nums, index):
    """
    Returns the most common bit found at the specified index in the provided
    list of bitarrays.
    """
    count0 = 0
    for num in nums:
        if num[index] == 0:
            count0 += 1

    if count0 > len(nums) / 2:
        return 0
    return 1

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        print('----- PART 1 -----')
        print(part1(processed))

        print('\n----- PART 2 -----')
        print(part2(processed))
