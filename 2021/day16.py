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


class Packet:
    def __init__(self, version, typeId) -> None:
        self.version = version
        self.typeId = typeId
        self.lenTypeId = None
        self._value = None
        self.subPackets = []
        self.bitLen = None

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: List[str]):
        self._value = ''.join(value)

    def __str__(self) -> str:
        if self.value:
            content = f'<value:{self.value}>'
        else:
            content = f'<{len(self.subPackets)} SubPackets>'
        return f'<Packet version:{self.version} typeId:{self.typeId} lenTypeId:{self.lenTypeId} contents:{content} bitLen:{self.bitLen}>'


def hex_to_bin(hexstr: str):
    return bin(int(hexstr, 16))[2:].rjust(len(hexstr)*4, '0')


def parse_packet(packet: str) -> Packet:
    # Uncomment to see process

    version = int(packet[0:3], 2)
    typeId = int(packet[3:6], 2)

    packetObj: Packet = Packet(version, typeId)

    # print('V:', version, '| T:', typeId)

    if typeId == 4:
        # Data packet
        values = []
        curr = 6
        while packet[curr] != '0':
            values.append(packet[curr+1:curr+5])
            curr += 5
        values.append(packet[curr+1:curr+5])
        packetObj.value = values
        packetObj.bitLen = curr+5
        return packetObj

    HEADER_OFFSET = 7

    packetObj.lenTypeId = packet[6]

    curr = None

    # print('I:', len_type_id)

    if packetObj.lenTypeId == '0':
        bitsToLook = 15
        lenInBits = int(packet[HEADER_OFFSET:HEADER_OFFSET+bitsToLook], 2)
        curr = HEADER_OFFSET+bitsToLook
        while curr < lenInBits+(HEADER_OFFSET+bitsToLook):
            subPacket: Packet = parse_packet(packet[curr:curr+lenInBits])
            packetObj.subPackets.append(subPacket)
            curr += subPacket.bitLen
    else:
        bitsToLook = 11
        totalSubPackets = int(
            packet[HEADER_OFFSET:HEADER_OFFSET+bitsToLook], 2)
        curr = HEADER_OFFSET+bitsToLook
        while totalSubPackets > 0:
            subPacket: Packet = parse_packet(packet[curr:])
            packetObj.subPackets.append(subPacket)
            curr += subPacket.bitLen
            totalSubPackets -= 1

    # print('LastBit:', curr)

    packetObj.bitLen = curr

    return packetObj


def sum_packet_versions(packet: Packet) -> int:
    if packet.typeId == 4:
        return packet.version

    total = packet.version

    for sp in packet.subPackets:
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
        print('ST:', syntax_tree)
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


def execute_packets(packet: Packet) -> Union[int, bool]:
    typeId = packet.typeId

    if typeId == 4:
        return int(packet.value, 2)

    if typeId == 0:
        # sum
        sumResult = 0
        for sp in packet.subPackets:
            sumResult += execute_packets(sp)
        return sumResult

    if typeId == 1:
        prodResult = 1
        for sp in packet.subPackets:
            prodResult *= execute_packets(sp)
        return prodResult

    if typeId == 2:
        minSp = None
        for sp in packet.subPackets:
            spRes = execute_packets(sp)
            if minSp is None or minSp > spRes:
                minSp = spRes
        return minSp

    if typeId == 3:
        maxSp = None
        for sp in packet.subPackets:
            spRes = execute_packets(sp)
            if maxSp is None or maxSp < spRes:
                maxSp = spRes
        return maxSp

    if typeId == 5:
        # greater than
        spRes1 = execute_packets(packet.subPackets[0])
        spRes2 = execute_packets(packet.subPackets[1])
        return spRes1 > spRes2

    if typeId == 6:
        # less than
        spRes1 = execute_packets(packet.subPackets[0])
        spRes2 = execute_packets(packet.subPackets[1])
        return spRes1 < spRes2

    if typeId == 7:
        # equal than
        spRes1 = execute_packets(packet.subPackets[0])
        spRes2 = execute_packets(packet.subPackets[1])
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
