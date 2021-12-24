import itertools
import sys
from collections import defaultdict
from math import floor, pow, sqrt


class Scanner:
    def __init__(self, id, points):
        self.id = id
        self.points = points
        self.distances = self.calculate_distances()
        self.orientations = {}
        self.overlaps = {}
        self.transformations = []
        self.path = []
        self.transformed_points = []

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

    # Testing/debugging helper
    def verify_overlap(self):
        for scanner in self.orientations:
            overlap = set(self.transformed_points).intersection(set(scanner.transformed_points))
            if not len(overlap) >= 12:
                print('ERROR: Expected overlap %d with scanner %d, found %d points of overlap' % (len(self.overlaps[scanner]), scanner.id, len(overlap)))
            else:
                print("Verified overlap of %d points with scanner %d" % (len(self.overlaps[scanner]), scanner.id))

    def transform_points(self):
        new_points = []
        for point in self.points:
            new_point = point
            for transformation in reversed(self.transformations):
                new_point = transform_point(new_point, *transformation)
            new_points.append(new_point)

        self.transformed_points = new_points
        return new_points

def get_distance(point1, point2):
    return sqrt(pow(point2[0] - point1[0], 2) + pow(point2[1] - point1[1], 2) + pow(point2[2] - point1[2], 2))

def get_manhattan_distance(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1]) + abs(point2[2] - point1[2])

def build(scanners):
    for i,j in itertools.combinations(range(len(scanners)), 2):
        find_overlap(scanners[i], scanners[j])
    build_transformations(scanners)

def find_overlap(scanner1, scanner2):
    overlap = set(scanner1.distances.keys()).intersection(set(scanner2.distances.keys()))

    # 66 is the number of unique distances with 12 points
    if len(overlap) >= 66:
        overlapping_points = []
        point_to_distances = defaultdict(list)
        for distance in overlap:
            points = scanner1.distances[distance]
            overlapping_points += points
            point_to_distances[points[0]].append(distance)
            point_to_distances[points[1]].append(distance)

        unique_overlaps = list(set([tuple(point) for point in overlapping_points]))

        # Build set of points in scanner 1
        point = unique_overlaps[0]
        to_match_points1 = [point]
        to_match_distances = []
        for _ in range(2):
            distance = point_to_distances[point][0]
            i = 1
            while distance in to_match_distances:
                distance = point_to_distances[point][i]
                i += 1

            to_match_distances.append(distance)
            next = scanner1.distances[distance][:]
            next.remove(point)
            to_match_points1.append(next[0])
            point = next[0]

        to_match_distances.append(set(point_to_distances[to_match_points1[0]]).intersection(set(point_to_distances[to_match_points1[2]])).pop())

        # Build set of points in scanner 2 based on distances
        first_pts = set(scanner2.distances[to_match_distances[0]][:])
        next_pts = set(scanner2.distances[to_match_distances[1]][:])
        to_match_points2 = list(first_pts.difference(next_pts)) + list(first_pts.intersection(next_pts)) + list(next_pts.difference(first_pts))

        # Set orientations both directions because we're not sure which will be the shorter path
        orientation1 = find_orientation(to_match_points1, to_match_points2)
        scanner2.set_orientation(scanner1, *orientation1)
        scanner2.overlaps[scanner1] = unique_overlaps

        orientation2 = find_orientation(to_match_points2, to_match_points1)
        scanner1.set_orientation(scanner2, *orientation2)
        scanner1.overlaps[scanner2] = unique_overlaps

def build_transformations(scanners):
    scanner = scanners[0]
    scanner.path = [scanner]
    to_visit = [scanner]
    visited = []
    while to_visit:
        next = to_visit.pop(0)
        visited.append(next)

        for scanner in next.orientations.keys():
            if not scanner in visited:
                scanner.transformations = next.transformations + [scanner.orientations[next]]
                scanner.path = next.path + [scanner]
                to_visit.append(scanner)

def transform_points(scanners):
    points = []
    for i in range(len(scanners)):
        points += scanners[i].transform_points()
    return points

def get_max_distance(scanners):
    locations = []

    for i in range(len(scanners)):
        # Shortcut to not have to calculate the location from the set of transformations
        _, _, location = find_orientation(scanners[i].transformed_points[:3], scanners[i].points[:3])
        locations.append([-1 * num for num in location])

    max_distance = 0
    pairs = itertools.combinations(locations, 2)
    for l1, l2 in pairs:
        distance = get_manhattan_distance(l1, l2)
        if distance > max_distance:
            max_distance = distance
    return max_distance

# How does scanner have to be oriented for these points to match up?
def find_orientation(points1, points2):
    permutations = list(itertools.permutations(range(3)))
    flips = list(itertools.product([-1, 1], repeat=3))
    for permutation in permutations:
        for flip in flips:
            all_match = True
            new_points = [transform_point(points2[i], permutation, flip) for i in range(3)]
            location = [0,0,0]
            for axis in range(3):
                distance = (points1[0][axis] - new_points[0][axis])
                for point_i in [1,2]:
                    if not (points1[point_i][axis] - new_points[point_i][axis]) == distance:
                        all_match = False
                        break
                if all_match:
                    location[axis] = distance

            if all_match:
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

        build(scanners)

        print('----- PART 1 -----')
        points = transform_points(scanners)
        print('Unique Points:', len(set(points)))

        print('----- PART 2 -----')
        max_dist = get_max_distance(scanners)
        print('Max Distance:', max_dist)
