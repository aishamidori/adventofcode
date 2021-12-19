import json
import sys
from copy import deepcopy
from functools import reduce
from itertools import combinations
from math import ceil, floor


def add(*numbers):
    root = BinaryNode(initial_value=None, parent=None, children=numbers)
    reduce_numbers(root)
    return root

def reduce_numbers(root):
    changed = True
    while changed:
        changed = False
        exploded = explode_all(root)
        split = split_first(root)
        changed = exploded or split

def split_first(root):
    # Check for any pairs that need to be split
    to_visit = [root]
    while to_visit:
        next = to_visit.pop(0)
        if next.int_value is not None and next.int_value >= 10:
            next.split()
            return True
        to_visit = next.children + to_visit
    return False

def explode_all(root):
    changed = True
    while changed:
        changed = False

        # Check for any pairs that need to be exploded
        to_visit = [root]
        while to_visit:
            next = to_visit.pop(0)

            if next.depth >= 4 and next.is_simple_pair():
                next.explode()
                changed = True
                break

            if next.is_pair():
                to_visit = next.children + to_visit

    return changed

class BinaryNode:
    def __init__(self, initial_value, parent=None, children=[]):
        self.initial_value = initial_value
        self.parent = parent

        # Source of truth for the regular number value
        self.int_value = self.initial_value if isinstance(self.initial_value, int) else None
        self.depth = self.parent.depth + 1 if self.parent else 0

        self.left = None
        self.right = None

        if children:
            self.left = children[0]
            self.right = children[1]
            for child in children:
                child.parent = self
                child.update_depth()

        elif isinstance(initial_value, list):
            self.left = BinaryNode(initial_value[0], parent=self)
            self.right = BinaryNode(initial_value[1], parent=self)

    def magnitude(self):
        if self.int_value is not None:
            return self.int_value
        elif self.left and self.right:
            return (3 * self.left.magnitude()) + (2 * self.right.magnitude())
        else:
            print('Error getting magnitude for', self)
            return -1

    def update_depth(self):
        self.depth = self.parent.depth + 1 if self.parent else 0
        for child in self.children:
            child.update_depth()

    def is_regular_number(self):
        return self.int_value is not None

    def is_pair(self):
        return self.int_value is None and self.left and self.right

    def is_simple_pair(self):
        return (self.int_value is None and
                self.left.int_value is not None and
                self.right.int_value is not None)

    def explode(self):
        assert self.depth >= 4 and self.is_simple_pair()

        # Check for next left regular number
        last_checked = self
        to_check = self.parent
        while to_check:
            if last_checked != to_check.left:
                if to_check.left and to_check.left.is_regular_number():
                    to_check.left.int_value += self.left.int_value

                to_check = to_check.left
                while to_check:
                    if to_check.right and to_check.right.is_regular_number():
                        to_check.right.int_value += self.left.int_value
                        break
                    to_check = to_check.right
                break

            last_checked = to_check
            to_check = to_check.parent


        # Check for next right regular number
        last_checked = self
        to_check = self.parent
        while to_check:
            if last_checked != to_check.right:
                if to_check.right and to_check.right.is_regular_number():
                    to_check.right.int_value += self.right.int_value

                to_check = to_check.right
                while to_check:
                    if to_check.left and to_check.left.is_regular_number():
                        to_check.left.int_value += self.right.int_value
                        break
                    to_check = to_check.left
                break

            last_checked = to_check
            to_check = to_check.parent

        # Replace this pair with the number 0
        self.left = None
        self.right = None
        self.int_value = 0

    def split(self):
        assert self.int_value >= 10

        # Turn this number into a pair
        self.left = BinaryNode(floor(self.int_value/2), parent=self)
        self.right = BinaryNode(ceil(self.int_value/2), parent=self)
        self.int_value = None

    @property
    def children(self):
        return [self.left, self.right] if self.left and self.right else []

    def __str__(self):
        return str(self.int_value) if self.int_value is not None else '[%s,%s]' % (str(self.left), str(self.right))


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        assert BinaryNode(json.loads("[[1,2],[[3,4],5]]")).magnitude() == 143
        assert BinaryNode(json.loads("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")).magnitude() == 3488
    else:
        numbers = []
        with open(sys.argv[1]) as f:
            root = None
            for line in f:
                parsed = json.loads(line)
                next_line = BinaryNode(parsed)
                numbers.append(next_line)

        print('----- PART 1 -----')
        # Kind of hacky to deep copy, but I'm modifying the tree for addition
        numbers1 = deepcopy(numbers)
        print(reduce(lambda x, y: add(x, y), numbers1).magnitude())

        print('----- PART 2 -----')
        max_sum = 0

        for i,j in combinations(range(len(numbers)), 2):
            sum = add(deepcopy(numbers[i]), deepcopy(numbers[j]))
            max_sum = max(sum.magnitude(), max_sum)

            # Order matters so try the other way too
            sum = add(deepcopy(numbers[j]), deepcopy(numbers[i]))
            max_sum = max(sum.magnitude(), max_sum)

        print(max_sum)
