import functools
import sys

def process(inputFile):
    all_groups = []
    curr_group = []
    for line in inputFile:
        #print(line.strip())
        if line == '\n':
            #print('END OF GROUP', curr_group)
            all_groups.append(curr_group)
            curr_group = []
        else:
            curr_group.append({char for char in line.strip()})
    all_groups.append(curr_group)

    print(all_groups)

    total = 0
    for group in all_groups:
        answers = set.intersection(*group)
        #print(''.join(answers))
        total = total + len(answers)

    print(total)


if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        inputFile = open(sys.argv[1])
        process(inputFile)
