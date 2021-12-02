from collections import defaultdict
from copy import copy, deepcopy
import sys

def get_slice(orig_list, from_i):
    removed = []
    while len(removed) < 3:
        if from_i >= len(orig_list):
            from_i = 0
        removed.append(orig_list.pop(from_i))
    return removed

def get_final_cups(cups):
    first_i = cups.index(1)
    num_cups = len(cups)
    print('next 2 numbers: %d, %d' % (cups[(first_i + 1)%num_cups], cups[(first_i + 2)%num_cups]))
    #return ''.join(str(cup) for cup in (cups[(first_i+1)%num_cups:] + cups[:first_i]))

def solve(arg, rounds):
    cups = [int(num) for num in arg]
    #cups += range(max(cups)+1, 1000000)
    cups_len = len(cups)
    max_num = max(cups)

    current_cup_i = 0
    current_cup = cups[current_cup_i]
    for round in range(int(rounds)):
        #print("\n-- move %d --" % (round+1))
        #print("cups:", " ".join(str(cup) for cup in cups))
        #print("current cup: %d" % current_cup)

        # Remove the next 3 clockwise cups
        removed_cups = [cups[(current_cup_i + i) % cups_len] for i in range(1, 4)]
        #print('removed:', removed_cups)

        #print("after removing:", " ".join(str(cup) for cup in cups))

        # Dest cup is the current cup label - 1
        dest_cup = current_cup - 1
        if dest_cup < 1:
            dest_cup = cups_len

        #print("Trying dest", dest_cup)
        while dest_cup in removed_cups:
            dest_cup -= 1
            if dest_cup < 1:
                dest_cup = cups_len

            #print("Dest cup is in the removed cups, trying", dest_cup)
        dest_i = cups.index(dest_cup)
        #print("adding cups after cup %d (index: %d)" % (dest_cup, dest_i))


        # Next 3 cups are placed immediately after the dest cup
        from_i = (current_cup_i + 4) % cups_len
        to_i = (current_cup_i + 1) % cups_len
        #print("Starting to update list with %d -> %d" % (from_i, to_i))
        while True:
            #print('from_i =', from_i, 'dest_i =', dest_i)
            #print('moving existing cups', to_i, '(out of %d)' % cups_len)
            cups[to_i] = cups[from_i]
            #print("cups:", " ".join(str(cup) for cup in cups))

            if cups[from_i] == current_cup:
                current_cup_i = to_i

            if cups[from_i] == dest_cup:
                # We've moved the destination cup, now we can just add our removed cups after it
                to_i = (to_i + 1) % cups_len
                break

            from_i = (from_i + 1) % cups_len
            to_i = (to_i + 1) % cups_len


        for cup in removed_cups:
            #print('adding removed cups', to_i, '(out of %d)' % cups_len)
            cups[to_i] = cup
            to_i = (to_i + 1) % cups_len
            #print("cups:", " ".join(str(cup) for cup in cups))

        #print("final cups:", " ".join(str(cup) for cup in cups))

        # Current cup is now the one to the right of the current cup
        current_cup_i = (current_cup_i + 1) % cups_len
        current_cup = cups[current_cup_i]

    #print('\n-- final --')
    #print("cups:", " ".join(str(cup) for cup in cups))

    return get_final_cups(cups)

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide an argument")
    else:
        print(solve(sys.argv[1], sys.argv[2]))
