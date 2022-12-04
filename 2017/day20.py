import sys
from typing import List

import numpy


def get_filename(test=False):
    return f'day20_input{"_test" if test else ""}.txt'


def get_input(parse, test=False):
    data = []
    filename = get_filename(test)
    with open(filename, "r") as file:
        for line in file:
            data.append(parse(line.strip()))
    return data


################################################################################
############################### Start of Part 1 ################################
################################################################################


def parse1(line: str):
    d = []
    div = 0
    for _ in range(3):
        div = line.index("=", div) + 2
        end = line.index(">", div)
        values = tuple(map(int, line[div:end].split(",")))
        d.append(values)

    return Particle(*d)


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def add(t_1: tuple, t_2: tuple):
    return tuple(sum(i) for i in zip(t_1, t_2))


class Particle:
    def __init__(self, x_0, v, a) -> None:
        self.x_0 = numpy.array(x_0)
        self.x = self.x_0.copy()
        self.v_0 = numpy.array(v)
        self.v = self.v_0.copy()
        self.acc = numpy.array(a)

    def manhattan_distance(self):
        return add(i for i in self.x)

    def position_at_frame(self, frame):
        return self.x_0 + (self.v_0 * frame) + (0.5 * (self.acc) * (frame * frame))

    def move(self):
        self.v += self.acc
        self.x += self.v
        return self.x

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return (
            "<Particle"
            f" x_0={self.x_0} x={self.x} v_0={self.v_0} v={self.v} a={self.acc}>"
        )


def manhattan_distance(vector):
    return sum(abs(i) for i in vector)


################################################################################


def day20p1():
    data: List[Particle] = get_input(parse1, test=False)
    min_acc = sys.maxsize
    closest_particle = None
    pid = None
    for i, particle in enumerate(data):
        acceleration_mag = sum(abs(i) for i in particle.acc)
        if acceleration_mag < min_acc:
            min_acc = acceleration_mag
            closest_particle = particle
            pid = i

    return pid, closest_particle


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################
def day20p2():
    particles: List[Particle] = get_input(parse2, test=True)
    positions = {}
    total_particles = len(particles)
    active_particles = [1 for _ in range(total_particles)]
    frame = 0
    while frame < 100:
        positions.clear()
        for pid in range(total_particles):
            if active_particles[pid] == 0:
                continue
            position: tuple = tuple(particles[pid].move())
            if position in positions:
                active_particles[pid] = 0
                active_particles[positions[position]] = 0
            else:
                positions[position] = pid
        frame += 1
    return sum(active_particles)


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1

    run_one = any(arg == "1" for arg in sys.argv)
    run_two = any(arg == "2" for arg in sys.argv)

    if run_one is False and run_two is False:
        run_one = run_two = True

    if run_one:
        print()
        print("-" * (n), "Day 20 - Part 1", "-" * n)
        print("Result =>", day20p1())
        print()
    if run_two:
        print("-" * (n), "Day 20 - Part 2", "-" * n)
        print("Result =>", day20p2())
    print()


main()
