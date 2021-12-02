import sys

PREAMBLE_LENGTH=25

def preprocess(file_path):
    nums = []
    with open(file_path) as f:
        for line in f:
            nums.append(int(line))
    return nums

def part1(nums):
    for i in range(PREAMBLE_LENGTH, len(nums)):
        num = nums[i]
        found_pair = False
        preamble = nums[(i-PREAMBLE_LENGTH):i]
        for prenum in preamble:
            if (num-prenum) in preamble:
                found_pair = True
                break
        if not found_pair:
            return num

TO_FIND = 14360655
def part2(nums):
    start = 0
    total = 0
    for i in range(len(nums)):
        end = i
        total = total + nums[i]
        while total > TO_FIND:
            total = total - nums[start]
            start = start + 1
        if total == TO_FIND:
            final_nums = nums[start:end+1]
            print(final_nums)
            assert sum(final_nums) == TO_FIND
            return min(final_nums) + max(final_nums)

if __name__ == "__main__":
    if not len(sys.argv) > 2:
        print("Please provide a file argument")
    else:
        PREAMBLE_LENGTH = int(sys.argv[2])
        output = preprocess(sys.argv[1])
        print(part1(output))
        print(part2(output))
