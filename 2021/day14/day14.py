from collections import defaultdict
import sys
import re

def preprocess(file_path):
    with open(file_path) as f:
        initial = f.readline().strip()

        # Blank line
        f.readline()

        rules = []
        for line in f:
            rules.append(line.strip().split(' -> '))
        return initial, rules

def part1(initial, rules, steps=10):
    #print('Template: %s' % initial)
    polymer = initial
    for step in range(1, steps + 1):
        to_add = ['' for _ in range(len(polymer))]
        for rule in rules:
            for match in re.finditer('(?=%s)' % rule[0], polymer):
                index = match.start()
                to_add[index] += rule[1]
        polymer = ''.join(map(lambda a: a[0] + a[1], list(zip(polymer, to_add))))
        #print('After step %d (len %d): %s' % (step, len(polymer), polymer))

    frequencies = defaultdict(int)
    for char in polymer:
        frequencies[char] += 1

    sorted_freqs = sorted(frequencies, key=frequencies.get)
    return frequencies[sorted_freqs[-1]] - frequencies[sorted_freqs[0]]

def part2(initial, rules, steps=40):
    pair_freqs = defaultdict(int)
    for i in range(len(initial) - 1):
        pair_freqs[initial[i:i+2]] += 1
    for step in range(steps):
        new_freqs = defaultdict(int)
        for rule in rules:
            if rule[0] in pair_freqs:
                count = pair_freqs[rule[0]]
                new_freqs[rule[0][0] + rule[1]] += count
                new_freqs[rule[1] + rule[0][1]] += count
        pair_freqs = new_freqs

    frequencies = defaultdict(int)
    for pair, freqs in pair_freqs.items():
        frequencies[pair[0]] += freqs
        frequencies[pair[1]] += freqs

    sorted_freqs = sorted(frequencies, key=frequencies.get)
    most_freq = frequencies[sorted_freqs[-1]]/2
    least_freq = frequencies[sorted_freqs[0]]/2

    return round(most_freq) - round(least_freq)


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('Please provide a file argument')
    else:
        initial, rules = preprocess(sys.argv[1])

        print('----- PART 1 -----')
        print(part1(initial, rules))

        print('----- PART 2 -----')
        print(part2(initial, rules))
