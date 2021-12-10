import sys

### CONSTANTS ###
SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

AUTOCOMPLETE_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

OPEN = '([<{'
CLOSED = ')]>}'

### HELPERS ###
def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        for line in f:
            processed.append(line.strip())
    return processed

def open_to_closed(c):
    return CLOSED[OPEN.index(c)]

def closed_to_open(c):
    return OPEN[CLOSED.index(c)]

# Returns (valid, incorrect_char). If line is valid, incorrect_char is the stack
def is_valid_line(line):
    #print(line)
    stack = []
    for i in range(len(line)):
        c = line[i]
        if c in OPEN:
            stack.append(c)
        elif c in CLOSED:
            opp = closed_to_open(c)
            if not stack or stack.pop() is not opp:
                #print("Not valid, unmatched %s" % c)
                return (False, c)

    return (True, stack)

### SOLUTIONS ###
def part1(processed):
    score = 0
    for line in processed:
        valid, incorrect_char = is_valid_line(line)
        if not valid:
            score += SCORES[incorrect_char]
    return score

def part2(processed):
    scores = []
    for line in processed:
        valid, incorrect_char = is_valid_line(line)
        if valid:
            total_score = 0
            while incorrect_char:
                unmatched_open = incorrect_char.pop()
                total_score *= 5
                total_score += AUTOCOMPLETE_SCORE[open_to_closed(unmatched_open)]
            scores.append(total_score)
    scores.sort()
    return scores[int(len(scores)/2)]

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])

        print('----- PART 1 -----')
        print(part1(processed))

        print('----- PART 2 -----')
        print(part2(processed))
