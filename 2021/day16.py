import functools
import queue
from types import FunctionType
from typing import List, Tuple, Union


def get_filename(test=False):
    return f'day16_input{"_test" if test else ""}.txt'


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
    return line

################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def hex_to_bin(hexstr: str):
    return bin(int(hexstr, 16))[2:].rjust(len(hexstr)*4, '0')


def parse_packet(packet: str) -> Tuple[int, int, Union[List[str], str], int]:
    # Uncomment to see process
    version = int(packet[0:3], 2)
    typeId = int(packet[3:6], 2)

    # print('V:', version, '| T:', typeId)

    if typeId == 4:
        # Data packet
        values = []
        curr = 6
        while packet[curr] != '0':
            values.append(packet[curr+1:curr+5])
            curr += 5
        values.append(packet[curr+1:curr+5])
        return (version, 4, ''.join(values), curr+5)

    HEADER_OFFSET = 7
    len_type_id = packet[6]
    subpackets = []
    curr = None

    # print('I:', len_type_id)

    if len_type_id == '0':
        bitsToLook = 15
        lenInBits = int(packet[HEADER_OFFSET:HEADER_OFFSET+bitsToLook], 2)
        curr = HEADER_OFFSET+bitsToLook
        while curr < lenInBits+(HEADER_OFFSET+bitsToLook):
            subPacket = parse_packet(packet[curr:curr+lenInBits])
            subpackets.append(subPacket)
            curr += subPacket[-1]
    else:
        bitsToLook = 11
        totalSubPackets = int(
            packet[HEADER_OFFSET:HEADER_OFFSET+bitsToLook], 2)
        curr = HEADER_OFFSET+bitsToLook
        while totalSubPackets > 0:
            subPacket = parse_packet(packet[curr:])
            subpackets.append(subPacket)
            curr += subPacket[-1]
            totalSubPackets -= 1

    # print('LastBit:', curr)

    return (version, typeId, subpackets, curr)


def sum_packet_versions(tree) -> int:
    if tree[1] == 4:
        return tree[0]

    total = tree[0]

    for sp in tree[2]:
        total += sum_packet_versions(sp)

    return total

################################################################################


def day16p1():
    packets = get_input(parse1, test=False)

    result = []
    for packet in packets:
        # print(packet, 'Len Original:', len(packet)*4)
        packet = hex_to_bin(packet)
        syntax_tree = parse_packet(packet)
        # print('ST:', syntax_tree)
        packetVersionSum = sum_packet_versions(syntax_tree)
        result.append(packetVersionSum)

    return list(map(lambda x: f'Sum: {x}', result))

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


def execute_packets(tree: tuple) -> Union[int, bool]:
    typeId = tree[1]

    if typeId == 4:
        return int(tree[2], 2)

    if typeId == 0:
        # sum
        sumResult = 0
        for sp in tree[2]:
            sumResult += execute_packets(sp)
        return sumResult

    if typeId == 1:
        prodResult = 1
        for sp in tree[2]:
            prodResult *= execute_packets(sp)
        return prodResult

    if typeId == 2:
        minSp = None
        for sp in tree[2]:
            spRes = execute_packets(sp)
            if minSp is None or minSp > spRes:
                minSp = spRes
        return minSp

    if typeId == 3:
        maxSp = None
        for sp in tree[2]:
            spRes = execute_packets(sp)
            if maxSp is None or maxSp < spRes:
                maxSp = spRes
        return maxSp

    if typeId == 5:
        # greater than
        spRes1 = execute_packets(tree[2][0])
        spRes2 = execute_packets(tree[2][1])
        return spRes1 > spRes2

    if typeId == 6:
        # less than
        spRes1 = execute_packets(tree[2][0])
        spRes2 = execute_packets(tree[2][1])
        return spRes1 < spRes2

    if typeId == 7:
        # equal than
        spRes1 = execute_packets(tree[2][0])
        spRes2 = execute_packets(tree[2][1])
        return spRes1 == spRes2

################################################################################


def day16p2():
    packets = get_input(parse2, test=False)
    results = []
    for packet in packets:
        packet = hex_to_bin(packet)
        st = parse_packet(packet)
        result = execute_packets(st)
        results.append(result)
    return 'Results:', results


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1
    print()
    print('-'*(n), "Day 16 - Part 1", '-'*n)
    print('Result =>', day16p1())
    print()
    print('-'*(n), "Day 16 - Part 2", '-'*n)
    print('Result =>', day16p2())
    print()


main()
