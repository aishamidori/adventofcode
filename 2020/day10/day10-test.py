import sys

def preprocess(file_path):
    adapters = []
    with open(file_path) as f:
        for line in f:
            adapters.append(int(line))
    sorted_adapters = sorted(adapters)
    sorted_adapters.append(sorted_adapters[-1] + 3)
    return sorted_adapters

def part1(adapters):
    print(adapters)
    result = 0
    differences = {}
    last = 0
    for i in range(len(adapters)):
        adapter = adapters[i]
        diff = adapter - last
        if diff in differences:
            differences[diff] = differences[diff] + 1
        else:
            differences[diff] = 1
        last = adapter

    print(differences)
    return differences[1] * differences[3]

def part2(adapters):
    adapters = [0] + adapters
    print(adapters)
    paths = [0 for _ in range(len(adapters))]
    paths[0] = 1
    for i in range(1, len(adapters)):
        #print('\n', '[', i, '] -', paths)
        path_count = 0
        prev_i = i - 1
        while prev_i >= 0:
            if adapters[i] - adapters[prev_i] <= 3:
                path_count = path_count + paths[prev_i]
            prev_i = prev_i - 1
        paths[i] = path_count
    return paths[-1]

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        #print(part1(processed))
        print(part2(processed))
