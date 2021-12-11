import sys

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        for line in f:
            pass
    return processed

def part1(processed):
    pass

def part2(processed):
    pass

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('Please provide a file argument')
    else:
        processed = preprocess(sys.argv[1])

        print('----- PART 1 -----')
        print(part1(processed))

        print('----- PART 2 -----')
        print(part2(processed))
