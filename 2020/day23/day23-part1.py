from collections import defaultdict
from copy import copy, deepcopy
import sys

def remove_3(orig_list, from_i):
    after_i = from_i + 3
    print(from_i, 'to', after_i)
    if after_i < len(orig_list):
        return orig_list[:from_i] + orig_list[after_i:]
    else:
        return orig_list[after_i%len(orig_list):from_i]

def get_slice(orig_list, from_i, to_i):
    listlen = len(orig_list)
    if to_i > listlen:
        return orig_list[from_i:] + orig_list[:(to_i%listlen)]
    else:
        return orig_list[from_i:to_i]

def get_final_cups(cups):
    first_i = cups.index(1)
    return ''.join(str(cup) for cup in (cups[first_i+1:] + cups[:first_i]))

def solve(arg, rounds):
    cups = [int(num) for num in arg]
    current_cup_i = 0
    current_cup = cups[current_cup_i]
    for round in range(int(rounds)):
        print("\n-- move %d --" % (round+1))
        print("cups:", " ".join(str(cup) for cup in cups))
        print("current cup: %d" % current_cup)

        # Remove the next 3 clockwise cups
        next_3 = get_slice(cups, current_cup_i+1, current_cup_i+4)
        print("picking up:", " ".join(str(cup) for cup in next_3))
        new_cups = remove_3(cups, current_cup_i+1)
        print("after removing:", " ".join(str(cup) for cup in new_cups))

        # Dest cup is the current cup label - 1
        dest_cup = current_cup - 1
        while not dest_cup in new_cups:
            dest_cup -= 1
            if dest_cup < min(new_cups):
                dest_cup = max(new_cups)

        # Next 3 cups are placed immediately after the dest cup
        dest_i = new_cups.index(dest_cup)
        print("putting them down after cup %d at index %d" % (dest_cup, dest_i))
        tmp_new = new_cups[:dest_i+1] + next_3
        if dest_i + 1 < len(new_cups):
            tmp_new += new_cups[dest_i+1:]
        new_cups = tmp_new

        # New cups are now the cups
        cups = new_cups

        # Current cup is now the one to the right of the current cup
        current_cup_i = (cups.index(current_cup) + 1) % len(cups)
        current_cup = cups[current_cup_i % len(cups)]

    return get_final_cups(cups)


if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide an argument")
    else:
        print(solve(sys.argv[1], sys.argv[2]))
