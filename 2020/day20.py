import collections
import math


def get_filename(test=False):
    return f'day20_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    filename = get_filename(test)
    with open(filename, 'r') as file:
        # for line in file:
        #     data.append(parse(line.strip()))
        return file.read().split('\n\n')

################################################################################
############################### Start of Part 1 ################################
################################################################################


def parse1(line):
    return line

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def getTileMap(lines):
    tile_map = {}
    for d in lines:
        tile_lines = d.split('\n')
        tile = tile_lines[0].replace('Tile ', '').replace(':', '').strip()
        tile_map[int(tile)] = tile_lines[1:]
    return tile_map


def getCorners(tiles):
    corners_map = collections.defaultdict(list)

    for id, tile in tiles.items():
        # insert four corners

        # up and down
        up = tile[0]
        down = tile[-1]

        # left and right
        left = ''.join([x[0] for x in tile])
        right = ''.join([x[-1] for x in tile])

        if up[::-1] in corners_map:
            corners_map[up[::-1]].append((id, 'up'))
        else:
            corners_map[up].append((id, 'up'))

        if down[::-1] in corners_map:
            corners_map[down[::-1]].append((id, 'down'))
        else:
            corners_map[down].append((id, 'down'))

        if right[::-1] in corners_map:
            corners_map[right[::-1]].append((id, 'right'))
        else:
            corners_map[right].append((id, 'right'))

        if left[::-1] in corners_map:
            corners_map[left[::-1]].append((id, 'left'))
        else:
            corners_map[left].append((id, 'left'))

    return corners_map
################################################################################


def day20p1():
    data = get_input(parse1, test=False)
    map_tiles = getTileMap(data)
    map_corners = getCorners(map_tiles)

    canvas_xy = int(math.sqrt(len(map_tiles)))

    canvas = [[None for _ in range(canvas_xy)]
              for _ in range(canvas_xy)]

    map_corners = list(filter(lambda crnr: len(
        crnr[1]) > 1, map_corners.items()))

    freq_id = collections.defaultdict(int)

    for corner in map_corners:
        ls_ids = corner[1]
        for id_ in ls_ids:
            freq_id[id_[0]] += 1

    result = 1
    # find ids which freq = 2
    for id, cnt in freq_id.items():
        if cnt == 2:
            result *= id

    return result

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def convertSideToCoord(side):
    if side == 'left':
        return (0, -1)
    if side == 'right':
        return (0, 1)
    if side == 'up':
        return (-1, 0)
    if side == 'down':
        return (1, 0)
    raise Exception('Invalid side', side)

# def rotateLeft(tile):


def rotateToMatch(tile1, tile2, side):

    return sideToMatch

################################################################################


def day20p2():
    data = get_input(parse2, test=True)
    map_tiles = getTileMap(data)
    map_corners = getCorners(map_tiles)

    monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

    canvas_xy = int(math.sqrt(len(map_tiles)))

    canvas = [[None for _ in range(canvas_xy)]
              for _ in range(canvas_xy)]

    map_corners = dict(filter(lambda crnr: len(
        crnr[1]) > 1, map_corners.items()))
    print(map_corners)

    freq_id = collections.defaultdict(int)

    for corner, ids in map_corners.items():
        for id_ in ids:
            freq_id[id_[0]] += 1

    # find a corner (0,0)
    c_0 = None
    for id, cnt in freq_id.items():
        if cnt == 2:
            c_0 = id
            break

    print('-'*20)
    nbs_map = collections.defaultdict(list)
    for _, ids in map_corners.items():
        for id in ids:
            x = set(ids)
            x.discard(id)
            nbs_map[id[0]].append((list(x)[0][0], id[1]))
    print(nbs_map)
    print(c_0)
    tm = {}
    canvas[0][0] = c_0
    s = [c_0]
    while len(s) != 0:
        currTile = s.pop()

        if currTile in tm:
            continue

        # do logic
        nb_ls = nbs_map[currTile]

        for nbs in nb_ls:

            s.append(nbs[0])

    # for x in range(canvas_xy):
    #     for y in range(canvas_xy):
    #         currTile = nbs_map[c_0]

    return 0


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 20 - Part 1", '-'*n)
    print('Result =>', day20p1())
    print()
    print('-'*(n), "Day 20 - Part 2", '-'*n)
    print('Result =>', day20p2())
    print()


main()
