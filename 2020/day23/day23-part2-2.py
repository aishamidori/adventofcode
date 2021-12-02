from collections import defaultdict
from copy import copy, deepcopy
import sys

class LinkedList:
    def __init__(self, values):
        self.first = None
        self.quick_lookup = {}
        prev = None
        self.max_value = 0
        for value in values:
            if value > self.max_value:
                self.max_value = value
            next = ListNode(value, prev=prev)
            if not self.first:
                self.first = next
            self.quick_lookup[value] = next
            if prev:
                prev.next = next
            prev = next

        # Circularly linked
        prev.next = self.first
        self.first.prev = prev

        self.length = len(values)

    def get(self, value):
        return self.quick_lookup[value]

    def contains(self, value):
        return value in self.quick_lookup

    def find(self, value):
        return self.quick_lookup[value]

    def remove(self, node):
        #print("removing %d", node.val)
        if node.prev:
            #print("Updating %d's next to %d" % (node.prev.val, node.next.val))
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        node.next = None
        node.prev = None

        #print(self.quick_lookup.keys())
        del self.quick_lookup[node.val]
        return node

    def add(self, node, after):
        node.next = after.next
        node.prev = after
        node.prev.next = node
        node.next.prev = node

        self.quick_lookup[node.val] = node
        return node

    def trace_last(self):
        ordered = []
        node = self.first.prev
        while node.prev:
            ordered.append(node.val)
            node = node.prev

            if node == self.first.prev:
                break

        return " ".join(str(num) for num in ordered)

    def __str__(self):
        ordered = []
        node = self.first
        while node.next:
            ordered.append(node.val)
            node = node.next

            # Since it's circularly linked, abort after we get all the way around
            if node == self.first:
                break

        return " ".join(str(num) for num in ordered)

class ListNode:
    def __init__(self, val, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev

    def __str__(self):
        return "Node val=%d, prev=%d, next=%d" % (self.val, self.prev.val, self.next.val)

def get_final_cups(cups):
    node = cups.find(1)
    first = node.next
    second = node.next.next
    print("Next two numbers: %d, %d" % (first.val, second.val))
    return first.val * second.val
    #return ''.join(str(cup) for cup in (cups[(first_i+1)%num_cups:] + cups[:first_i]))

def solve(arg, rounds):
    cups = LinkedList([int(num) for num in arg] + list(range(len(arg) + 1, 1000001)))
    print("Finished creating start list")
    current_cup = cups.first
    for round in range(int(rounds)):
        #print("\n-- move %d --" % (round+1))
        #print("cups:", str(cups))
        #print("current cup: %d" % current_cup.val)

        # Remove the next 3 clockwise cups
        removed_cups = []
        #print("trace_last:", cups.trace_last())
        for _ in range(3):
            removed_cups.append(cups.remove(current_cup.next))
        #print('removed:', [cup.val for cup in removed_cups])

        #print("after removing:", str(cups))

        # Dest cup is the current cup label - 1
        dest_cup_val = current_cup.val - 1
        if dest_cup_val < 1:
            dest_cup_val = cups.max_value

        #print("Trying dest", dest_cup)
        while not cups.contains(dest_cup_val):
            dest_cup_val -= 1
            if dest_cup_val < 1:
                dest_cup_val = cups.max_value

            #print("Dest cup is in the removed cups, trying", dest_cup)
        dest_node = cups.get(dest_cup_val)
        #print("adding cups after cup %d" % (dest_cup_val))

        after = dest_node
        for cup in removed_cups:
            after = cups.add(cup, after=after)

        #print("cups:", str(cups))

        # Current cup is now the one to the right of the current cup
        current_cup = current_cup.next

    #print("\n-- final --")
    #print("cups:", str(cups))
    return get_final_cups(cups)

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide an argument")
    else:
        print(solve(sys.argv[1], sys.argv[2]))
