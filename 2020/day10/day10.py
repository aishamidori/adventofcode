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
    return get_num_combos(adapters, [])

paths = []

def get_num_combos(adapters, path):
    #print(adapters)
    #print(path)
    adapter = adapters[0]
    path = path + [adapter]
    if len(adapters) == 1:
        #complete path
        paths.append(path)
        #print(path)
    for i in range(1, len(adapters)):
        next_adapter = adapters[i]
        if next_adapter - adapter <= 3:
            # valid
            get_num_combos(adapters[i:], path + [next_adapter])
        else:
            break
    return len(paths)

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        #print(part1(processed))
        print(part2(processed))
