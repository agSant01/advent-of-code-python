import collections
import queue
from typing import List, Set


def get_filename(test=False):
    return f'day19_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, 'r') as file:
        for line in file:
            data.append(parse(line.strip()))
    return data

################################################################################
############################### Start of Part 1 ################################
################################################################################


def parse1(line: str):
    if len(line) == 0:
        return None
    if 'scanner' in line:
        return line
    return tuple(map(int, line.split(',')))

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def parse_beacon(data: List[str]) -> List[List[str]]:
    scanner_list = []
    beacon_set = []
    i = 0
    for line in data[1:]:
        if line == None:
            continue
        if 'scanner' in line:
            scanner_list.append((i, beacon_set))
            beacon_set = []
            i += 1
        else:
            beacon_set.append(line)

    scanner_list.append((i, beacon_set))

    return scanner_list


M = {
    0: lambda x, y, z: (x, y, z),
    1: lambda x, y, z: (x, z, -y),
    2: lambda x, y, z: (x, -y, -z),
    3: lambda x, y, z: (x, -z, y),
    4: lambda x, y, z: (y, x, -z),
    5: lambda x, y, z: (y, z, x),
    6: lambda x, y, z: (y, -x, z),
    7: lambda x, y, z: (y, -z, -x),
    8: lambda x, y, z: (z, x, y),
    9: lambda x, y, z: (z, y, -x),
    10: lambda x, y, z: (z, -x, -y),
    11: lambda x, y, z: (z, -y, x),
    12: lambda x, y, z: (-x, y, -z),
    13: lambda x, y, z: (-x, z, y),
    14: lambda x, y, z: (-x, -y, z),
    15: lambda x, y, z: (-x, -z, -y),
    16: lambda x, y, z: (-y, x, z),
    17: lambda x, y, z: (-y, z, -x),
    18: lambda x, y, z: (-y, -x, -z),
    19: lambda x, y, z: (-y, -z, x),
    20: lambda x, y, z: (-z, x, -y),
    21: lambda x, y, z: (-z, y, x),
    22: lambda x, y, z: (-z, -x, y),
    23: lambda x, y, z: (-z, -y, -x),
}


def rotate(coordinates: list, i):
    rt = M[i]
    res = []
    for coordinate in coordinates:
        res.append(rt(*coordinate))
    return res


def has_intersection(origin, target, origin_loc):
    for beacon1 in origin:
        # print('B1', beacon1)
        for i in range(24):
            rotated_beacons = rotate(target, i)
            for rb in rotate(target, i):
                tx = beacon1[0] - rb[0]
                ty = beacon1[1] - rb[1]
                tz = beacon1[2] - rb[2]
                trans_beacons_2 = set([(bx + tx, by + ty, bz + tz)
                                       for bx, by, bz in rotated_beacons])
                if len(trans_beacons_2.intersection(origin)) >= 12:
                    return True, rotated_beacons, (origin_loc[0] + tx, origin_loc[1]+ty, origin_loc[2] + tz)

    return False, None,  None


################################################################################


def day19p1():
    data = get_input(parse1, test=False)

    sclist = parse_beacon(data)

    locations = {0: (0, 0, 0)}
    planes = {0: sclist[0][1]}
    sclist = sorted(sclist, key=lambda x: x[1], reverse=True)

    q = queue.Queue()
    for i in sclist:
        q.put(i)

    has_int = False
    while q.qsize() > 0:
        i, scanner1 = q.get()
    # for i, scanner1 in enumerate(sclist):
        # print(scanner1)
        # print('i', i, scanner1)
        # print('i', i)
        for j, scanner2 in planes.items():
            # print(j)
            has_int, rotated_plane, location = has_intersection(
                scanner2, scanner1, locations[j])
            if has_int:
                print('Intersection found...', f'{j} => {i}')
                locations[i] = location
                planes[i] = rotated_plane
                break

        if not has_int:
            q.put((i, scanner1))

        # print('plane', planes.keys(), 'loc', locations)

    total_beacons = set()
    for i, location in locations.items():
        plane = planes[i]
        total_beacons.update(
            [(x+location[0], y+location[1], z+location[2]) for x, y, z in plane])

    return len(total_beacons), locations


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def max_manhattan(coordinates: list):
    maximum = 0

    N = len(coordinates)
    for i in range(N):
        sum = 0
        for j in range(i + 1, N):

            # Find Manhattan distance
            # using the formula
            # |x1 - x2| + |y1 - y2|
            sum = (abs(coordinates[i][0] - coordinates[j][0]) +
                   abs(coordinates[i][1] - coordinates[j][1]) +
                   abs(coordinates[i][2] - coordinates[j][2]))

            # Updating the maximum
            maximum = max(maximum, sum)

    return maximum


################################################################################


def day19p2(part1_result):
    locations: dict = part1_result[1]
    return max_manhattan(list(locations.values()))


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 19 - Part 1", '-'*n)
    result1 = day19p1()
    print('Result =>', result1)
    print()
    print('-'*(n), "Day 19 - Part 2", '-'*n)
    print('Result =>', day19p2(result1))
    print()


main()
