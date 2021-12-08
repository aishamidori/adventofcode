import sys

def preprocess(file_path):
    entries = []
    with open(file_path) as f:
        for line in f:
            split = line.strip().split('|')
            patterns = split[0].strip().split()
            output_value = split[1].strip().split()
            entries.append((patterns, output_value))
    return entries

def part1(entries):
    count = 0
    for entry in entries:
        patterns, output_value = entry
        for pattern in output_value:
            num = get_num(pattern)
            print("%s -> %s" % (pattern, str(num)))
            if num:
                count += 1
    return count

def part2(entries):
    total = 0
    for entry in entries:
        total += solve_entry(*entry)

    return total

def solve_entry(patterns, output_value):
    print("\n")
    print("|".join([" ".join(patterns), " ".join(output_value)]))
    patterns.sort(key=len)
    nums = [None for _ in range(10)]

    # 1 has 2 segments
    nums[1] = set(patterns[0])

    # 7 has 3 sements
    nums[7] = set(patterns[1])

    # 4 has 4 segments
    nums[4] = set(patterns[2])

    # 8 has 7 segments
    nums[8] = set(patterns[9])

    for i in range(3, 9):
        pattern = patterns[i]
        if len(pattern) == 5:
            if len(set(pattern).intersection(nums[1])) == 2:
                nums[3] = set(pattern)
            elif len(set(pattern).intersection(nums[4])) == 3:
                nums[5] = set(pattern)
            else:
                nums[2] = set(pattern)
        elif len(pattern) == 6:
            if len(set(pattern).intersection(nums[4])) == 4:
                nums[9] = set(pattern)
            elif len(set(pattern).intersection(nums[1])) == 2:
                nums[0] = set(pattern)
            else:
                nums[6] = set(pattern)
        else:
            print("ERROR")

    final_num = ''
    for val in output_value:
        num = nums.index(set(val))
        print("%s -> %d" % (val, num))
        final_num += str(num)
    return int(final_num)

def get_num(pattern):
    unique_chars = len(set(pattern))
    if unique_chars == 2:
        return 1
    elif unique_chars == 4:
        return 4
    elif unique_chars == 3:
        return 7
    elif unique_chars == 7:
        return 8
    else:
        return None

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        entries = preprocess(sys.argv[1])

        print('----- PART 1 -----')
        print(part1(entries))

        print('----- PART 2 -----')
        print(part2(entries))
