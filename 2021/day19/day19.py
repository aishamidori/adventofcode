import itertools
import sys
from collections import defaultdict
from functools import reduce
from math import floor, pow, sqrt


class Scanner:
    def __init__(self, id, points):
        self.id = id
        self.points = points
        self.distances = self.calculate_distances()
        self.orientations = {}
        self.transformations = []
        self.path = []

    def calculate_distances(self):
        distances = {}
        for i,j in list(itertools.combinations(range(len(self.points)), 2)):
            distance = get_distance(self.points[i], self.points[j])
            distances[distance] = [self.points[i], self.points[j]]
        return distances

    def set_orientation(self, based_on, permutation, flip, location):
        self.orientations[based_on] = (permutation, flip, location)

    def print_transformations(self):
        print("\n".join(['scanner %d -- p=%s, f=%s, l=%s --> scanner %d' % (scanner.id, self.orientations[scanner][0], self.orientations[scanner][1], self.orientations[scanner][2], self.id) for scanner in self.orientations.keys()]))

    def transformed_points(self):
        #print('transformations for scanner %d' % self.id, self.transformations)
        new_points = []
        for point in self.points:
            new_point = reduce(lambda point, transformation: transform_point(point, *transformation), self.transformations, point)
            new_points.append(new_point)
        return new_points

def get_distance(point1, point2):
    return sqrt(pow(point2[0] - point1[0], 2) + pow(point2[1] - point1[1], 2) + pow(point2[2] - point1[2], 2))

def find_overlap(scanners):
    for i,j in itertools.combinations(range(len(scanners)), 2):
        scanner1 = scanners[i]
        scanner2 = scanners[j]
        overlap = set(scanner1.distances.keys()).intersection(set(scanner2.distances.keys()))

        # 66 is the number of unique distances with 12 points
        if len(overlap) >= 66:
            print(len(overlap))
            overlapping_points = []
            point_to_distances = defaultdict(list)
            for distance in overlap:
                points = scanner1.distances[distance]
                overlapping_points += points
                point_to_distances[points[0]].append(distance)
                point_to_distances[points[1]].append(distance)

            unique_overlaps = list(set([tuple(point) for point in overlapping_points]))

            point = unique_overlaps[0]
            to_match_points1 = [point]
            to_match_distances = []

            for _ in range(2):
                distance = point_to_distances[point][0]
                to_match_distances.append(distance)
                next = scanner1.distances[distance][:]

                next.remove(point)
                to_match_points1.append(next[0])
                point = next[0]

            to_match_distances.append(set(point_to_distances[to_match_points1[0]]).intersection(set(point_to_distances[to_match_points1[2]])).pop())

            first_pts = set(scanner2.distances[to_match_distances[0]][:])
            next_pts = set(scanner2.distances[to_match_distances[1]][:])
            to_match_points2 = list(first_pts.difference(next_pts)) + list(first_pts.intersection(next_pts)) + list(next_pts.difference(first_pts))

            orientation = find_orientation(to_match_points1, to_match_points2)
            scanner2.set_orientation(scanner1, *orientation)

            orientation = find_orientation(to_match_points2, to_match_points1)
            scanner1.set_orientation(scanner2, *orientation)

            print("\nScanners %d and %d overlap by %d points" % (scanner1.id, scanner2.id, len(unique_overlaps)))
            #print("Overlapping points: %s" % '\n\t'.join([','.join([str(num) for num in point]) for point in unique_overlaps]))

    scanner = scanners[0]
    scanner.path = [scanner]
    to_visit = [scanner]
    visited = []
    while to_visit:
        next = to_visit.pop(0)
        visited.append(next)

        for scanner in next.orientations.keys():
            if not scanner in visited:
                scanner.transformations = [scanner.orientations[next]] + next.transformations
                scanner.path = next.path + [scanner]
                to_visit.append(scanner)

    points = []
    for i in range(len(scanners)):
        print('----- SCANNER %d -----' % scanners[i].id)
        #scanners[i].print_transformations()
        print(' -> '.join([str(scanner.id) for scanner in scanners[i].path]))
        #print(scanners[i].transformations)
        scanner_loc = [0,0,0]
        for permutation, flip, location in scanners[i].transformations:
            for j in range(3):
                scanner_loc[j] = scanner_loc[j] + location[j]

        transformed = scanners[i].transformed_points()
        for j in range(len(transformed)):
            print('%s -> %s' % (','.join([str(num) for num in scanners[i].points[j]]), ','.join([str(num) for num in transformed[j]])))
        points += transformed
        if not scanners[i].orientations:
            print("ERROR scanner %d doesn't have neighbors" % i)
            return

    print("ALL POINTS")
    print('\n'.join([','.join([str(num) for num in point]) for point in sorted(set(points))]))
    print(len(set(points)))


# How does scanner have to be oriented for these points to match up?
def find_orientation(points1, points2):
    permutations = list(itertools.permutations(range(3)))
    flips = list(itertools.product([-1, 1], repeat=3))
    for permutation in permutations:
        #print('permutation', permutation)
        for flip in flips:
            #print('flip', flip)
            all_match = True
            new_point0 = transform_point(points2[0], list(permutation), list(flip))
            new_point1 = transform_point(points2[1], list(permutation), list(flip))
            location = [0,0,0]
            for axis in range(3):
                if (new_point1[axis]- points1[1][axis]) == (new_point0[axis] - points1[0][axis]):
                    location[axis] = points1[1][axis] - new_point1[axis]
                else:
                    #print('Orientation doesn\'t work')
                    all_match = False
                    break

            if all_match:
                print('Found orientation %s -> %s and %s -> %s' % (str(new_point0), str(points1[0]), str(new_point1), str(points1[1])))
                print('location', location)
                return (permutation, flip, tuple(location))
    return (None, None, None)

# Inputs should be in the following format:
#   permutation: [2,1,0] (the order to scramble the axes)
#   flips: [-1, 1, -1] (which axes to flip)
#   location: [100, 10, -30] (how far to move the scanner on each axis)
#
# Axis order is applied first, then flips
def transform_point(point, permutation, flips, location=[0,0,0]):
    final_point = []
    for i in range(3):
        final_point.append((point[permutation[i]] * flips[i]) + location[i])
    #print('transformed point %s with p=%s, f=%s, l=%s -----> %s' % (str(point), str(permutation), str(flips), str(location), str(final_point)))
    return tuple(final_point)

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        # Test distance
        assert floor(get_distance([404,-588,-901], [528,-643,409])) == 1317

        # Test getting orientation
        original_points = [(1, 3, 4), (-5, 6, -75), (1301,-523, 0)]
        transformed_points = [(-5, 13, 300), (74, 16, 306), (-1, -513, -1000)]
        permutation = (2, 1, 0)
        flips = (-1, 1, -1)
        location = (-1, 10, 301)

        for i in range(3):
            rotated = transform_point(original_points[i], permutation, flips, location)
            assert transformed_points[i] == rotated

        (calced_permutation, calced_flips, calced_loc) = find_orientation(transformed_points, original_points)

        assert calced_permutation == permutation
        assert calced_flips == flips
        assert calced_loc == location

    else:
        scanners = []
        with open(sys.argv[1]) as f:
            while True:
                line = f.readline().strip()
                if not line:
                    break

                number = line[12:].split()[0]
                beacons = []
                for line in f:
                    if not line.strip():
                        break

                    beacons.append(tuple([int(num) for num in line.strip().split(',')]))

                scanners.append(Scanner(int(number), beacons))

        print('----- PART 1 -----')
        find_overlap(scanners)
        #print('----- PART 2 -----')
