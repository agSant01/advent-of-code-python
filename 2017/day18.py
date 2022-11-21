import collections
import sys


def get_filename(test=False):
    return f'day18_input{"_test" if test else ""}.txt'


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


def parse1(line):
    return line.split()


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################
"""
There aren't that many instructions, so it shouldn't be hard to figure out what they do. Here's what you determine:

# snd X plays a sound with a frequency equal to the value of X.
set X Y sets register X to the value of Y.
add X Y increases register X by the value of Y.
mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
Many of the instructions can take either a register (a single letter) o
"""


def is_register(value):
    return str(value).isalpha()


def execute_instructions(instructions, registers, pc=0):
    last_played_sound = None
    while pc < len(instructions):
        opcode, *values = instructions[pc]
        # print(opcode, values, registers, pc)

        if opcode == 'rcv':
            to_cmp = registers[values[0]]
            if to_cmp > 0:
                return {
                    'rcv': last_played_sound
                }
        elif opcode == 'snd':
            # play sound
            last_played_sound = registers[values[0]]
        else:
            if is_register(values[1]):
                value_to_use = registers[values[1]]
            else:
                value_to_use = int(values[1])

            if opcode == 'set':
                registers[values[0]] = value_to_use
            elif opcode == 'add':
                registers[values[0]] += value_to_use
            elif opcode == 'mul':
                registers[values[0]] *= value_to_use
            elif opcode == 'mod':
                registers[values[0]] %= value_to_use
            elif opcode == 'jgz':
                if is_register(values[0]):
                    conditional = registers[values[0]]
                else:
                    conditional = int(values[0])

                if conditional > 0:
                    pc += value_to_use
                    continue
        pc += 1
################################################################################


def day18p1():
    data = get_input(parse1, test=False)
    registers = collections.defaultdict(int)
    pc = 0
    pc = execute_instructions(data, registers, pc)
    return pc

################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)

################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


class Sockets():
    def __init__(self) -> None:
        self.messages = collections.defaultdict(list)
        self.msg_count = collections.defaultdict(int)

    def send(self, message, to_program_id: int, by_pid: int):
        print(f'[PID:{by_pid}] Send to PID: {to_program_id} | Msg: {message}')
        self.messages[to_program_id].insert(0, message)
        self.msg_count[by_pid] += 1

    def rcv(self, program_id: int):
        print(f'[PID:{program_id}] Reading from message queue...')
        return self.messages[program_id].pop()

    def has_msg(self, program_id: int):
        return len(self.messages[program_id]) > 0

    def __repr__(self) -> str:
        return f'<Sockets messages={self.messages} msg_count={self.msg_count}>'


class DeadlockDetector:
    def __init__(self, pids=[]) -> None:
        self.pids = dict((pid, False) for pid in pids)
        self.cnt = 0

    def has_deadlock(self):
        self.cnt += int(all(x for x in self.pids.values()))
        # print(self.pids, self.cnt)
        if self.cnt > 2:
            return True
        return False

    def waiting_rcv(self, pid: int):
        self.pids[pid] = True

    def exit_rcv(self, pid: int):
        self.pids[pid] = False
        self.cnt = 0

    def __repr__(self) -> str:
        return f'<DeadlockDetector pids_waiting_status={self.pids}>'


def execute_program(program_id: int, parallel_program_id: int, sockets: Sockets,
                    instructions, registers, deadlock_detector: DeadlockDetector, pc):
    print(f'[PID:{program_id}] Resumed Process...')
    while pc < len(instructions):
        if deadlock_detector.has_deadlock():
            break
        opcode, *values = instructions[pc]
        # print(opcode, values, registers, pc)
        if opcode == 'rcv':
            deadlock_detector.waiting_rcv(program_id)
            if sockets.has_msg(program_id):
                rcv_msg = sockets.rcv(program_id)
                registers[values[0]] = rcv_msg
                deadlock_detector.exit_rcv(program_id)
            else:
                print(f'[PID:{program_id}] No msg. waiting....')
                break
        elif opcode == 'snd':
            # play sound
            if is_register(values[0]):
                vtu = registers[values[0]]
            else:
                vtu = int(values[0])
            sockets.send(vtu, parallel_program_id, program_id)
        else:
            if is_register(values[1]):
                value_to_use = registers[values[1]]
            else:
                value_to_use = int(values[1])

            if opcode == 'set':
                registers[values[0]] = value_to_use
            elif opcode == 'add':
                registers[values[0]] += value_to_use
            elif opcode == 'mul':
                registers[values[0]] *= value_to_use
            elif opcode == 'mod':
                registers[values[0]] %= value_to_use
            elif opcode == 'jgz':
                if is_register(values[0]):
                    conditional = registers[values[0]]
                else:
                    conditional = int(values[0])

                if conditional > 0:
                    pc += value_to_use
                    continue
        pc += 1
    return pc

################################################################################


def day18p2():
    data = get_input(parse2, test=False)

    deadlock_detector = DeadlockDetector([0, 1])
    sockets = Sockets()

    pc_a = 0
    registers_a = collections.defaultdict(int)
    registers_a['p'] = 0
    pc_a = execute_program(0, 1, sockets, data,
                           registers_a, deadlock_detector, pc_a)

    pc_b = 0
    registers_b = collections.defaultdict(int)
    registers_b['p'] = 1
    pc_b = execute_program(1, 0, sockets, data,
                           registers_b, deadlock_detector, pc_b)

    while not deadlock_detector.has_deadlock():
        print(sockets)
        pc_a = execute_program(0, 1, sockets, data,
                               registers_a, deadlock_detector, pc_a)
        print(sockets)
        pc_b = execute_program(1, 0, sockets, data,
                               registers_b, deadlock_detector, pc_b)

    return sockets.msg_count


def main():
    divs = 40
    msg = 15
    n = (divs-msg)//2
    divs += 1

    run_one = any(arg == "1" for arg in sys.argv)
    run_two = any(arg == "2" for arg in sys.argv)

    if run_one is False and run_two is False:
        run_one = run_two = True

    if run_one:
        print()
        print('-'*(n), "Day 18 - Part 1", '-'*n)
        print('Result =>', day18p1())
        print()
    if run_two:
        print('-'*(n), "Day 18 - Part 2", '-'*n)
        print('Result =>', day18p2())
    print()


main()
