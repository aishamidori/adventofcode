import sys

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        for line in f:
            processed.append(int(line))
    return processed

def part1(processed):
    last = None
    increases = 0
    for line in processed:

        # Skip the first one, not really the most efficient way to do this
        # Then, increment our `increases` counter if the current line is greater than the last one
        if last and line > last:
            increases += 1

        # Whether or not it's greater, keep track of the current line which will be come `last` for the next iteration of the loop
        last = line

    return increases


def part2(processed):
    increases = 0

    # Slightly different tactic for this one, we're going to iterate by indices this time instead
    for i in range(len(processed)):

        # The only difference between the last sliding window and this one is the number 3 back not being included and the new one being added.
        # So, if the new one we're adding is larger than the one 3 back, the window sum will increase.
        if processed[i - 3] < processed[i]:
            increases += 1

    return increases

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('Please provide a file argument')
    else:
        processed = preprocess(sys.argv[1])
        #print(part1(processed))
        print(part2(processed))
