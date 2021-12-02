from collections import defaultdict
import sys

def preprocess(file_path):
    nums = None
    with open(file_path) as f:
        line = f.readline()
        nums = [int(num) for num in line.split(',')]
    return nums

def part1(processed):
    record = []
    starting = processed[:]

    last = None
    num = None

    for i in range(2020):
        num = 0
        if len(starting):
            num = starting[0]
            starting = starting[1:]
        elif last in record:
            penultimate = None
            for j in range(len(record) - 1, -1, -1):
                if record[j] == last:
                    #print('Found previous instance at', j, '- num =', len(record), '-', j, '=', len(record) - j)
                    num = len(record) - j
                    break

        print('Turn', i, ':', num)
        record.append(last)
        last = num

    return num

def part2(processed):
    starting = processed[:]
    indices = defaultdict(lambda: [])

    last = None
    num = None

    for i in range(30000000):
        num = 0
        #print('instances of last number', last, '-', indices[last])
        if len(starting):
            num = starting[0]
            starting = starting[1:]
        elif len(indices[last]) > 1:
            #print('last index', indices[last][-1])
            num = indices[last][-1] - indices[last][-2]

        print('Turn', i, ':', num)
        indices[num].append(i + 1)
        if len(indices[num]) > 2:
            indices[num] = indices[num][-2:]
        last = num
    return num

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        #print(part1(processed))
        print(part2(processed))
