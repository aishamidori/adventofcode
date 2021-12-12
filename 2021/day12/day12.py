from enum import Enum
import sys


class Size(Enum):
    SMALL = 2
    LARGE = 1

class Cave:
    def __init__(self, name):
        self.name = name
        self.paths = []

    @property
    def size(self):
        if self.name.isupper():
            return Size.LARGE
        return Size.SMALL

    def add_path(self, cave):
        self.paths.append(cave)

    def __str__(self):
        return ('%s -> %s' % (self.name, ','.join([cave.name for cave in self.paths])))

def preprocess(file_path):
    caves = {}
    with open(file_path) as f:
        for line in f:
            split = line.strip().split('-')
            for i in range(2):
                name = split[i]
                if not name in caves:
                    caves[name] = Cave(name)
            caves[split[0]].add_path(caves[split[1]])
            caves[split[1]].add_path(caves[split[0]])
    return caves

def part1(caves):
    current = caves['start']
    paths = follow_path(caves, [], [], current)
    path_strs = []
    for path in paths:
        path_strs.append(','.join([cave.name for cave in path]))
    path_strs.sort()
    print('\n'.join(path_strs))
    return len(paths)

def follow_path(caves, visited_small, path, current):
    path = path + [current]
    paths = []
    for next in current.paths:
        if next.name == 'start':
            continue
        if next.name == 'end':
            paths.append(path + [next])
            continue

        if not next in visited_small:
            next_visited_small = visited_small[:]
            if next.size == Size.SMALL:
                next_visited_small.append(next)
            paths += follow_path(caves, next_visited_small, path, next)
    return paths

def part2(caves):
    current = caves['start']
    paths = follow_path2(caves, [], False, [], current)
    path_strs = []
    for path in paths:
        path_strs.append(','.join([cave.name for cave in path]))
    path_strs.sort()
    print('\n'.join(path_strs))
    return len(paths)

def follow_path2(caves, visited_small, double_visited, path, current):
    path = path + [current]
    paths = []
    for next in current.paths:
        if next.name == 'start':
            continue
        if next.name == 'end':
            paths.append(path + [next])
            continue

        if not next in visited_small:
            next_visited_small = visited_small[:]
            if next.size == Size.SMALL:
                next_visited_small.append(next)
            paths += follow_path2(caves, next_visited_small, double_visited, path, next)
        elif not double_visited:
            paths += follow_path2(caves, visited_small, True, path, next)

    return paths


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('Please provide a file argument')
    else:
        processed = preprocess(sys.argv[1])

        print('----- PART 1 -----')
        print(part1(processed))

        print('----- PART 2 -----')
        print(part2(processed))
