import collections


def get_filename(test=False):
    return f'day14_input{"_test" if test else ""}.txt'


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
    line = (
        line.replace("seconds, but then must rest for", "")
        .replace("can fly", "")
        .replace("km/s for", "")
        .replace("seconds", "")
        .replace(".", "")
        .strip()
        .split()
    )
    reindeer, speed, run_time, rest_time = line
    return (reindeer, int(speed), int(run_time), int(rest_time))


################################################################################
########################## Helper Functions of Part 1 ##########################
################################################################################


def calculate_distance(reindeer_info, race_time):
    # Time: O(RaceTime / (RunTime + WaitTime)) Version1
    # Time: O(1) // Improved Version2
    # Mem: O(1)
    _, speed, run_t, rest_t = reindeer_info
    cycle_t = run_t + rest_t

    # START BLOCK
    """
    # Version1 Implementation: Linear Time O(n)
    # Found a better way, making it Constant Time.  O(1)
    # See below:
    """
    # runing_seconds = 0
    # while race_time > run_t:
    #     runing_seconds += run_t  # add running seconds
    #     race_time -= cycle_t  # decrease running and waiting time

    # if race_time > 0:
    #   runing_seconds += race_time
    # END BLOCK

    cycles = race_time // cycle_t
    runing_seconds = cycles * run_t + min(run_t, race_time % cycle_t)

    return runing_seconds * speed


################################################################################
def day14p1():
    is_test = False
    data = get_input(parse1, test=is_test)
    result = []

    total_time = 1000 if is_test else 2503

    for d in data:
        print(d)
        dist = calculate_distance(d, total_time)
        result.append((d[0], dist))

    print(result)

    return max(map(lambda x: x[1], result))


################################################################################
############################### Start of Part 2 ################################
################################################################################


def parse2(line):
    return parse1(line)


################################################################################
########################## Helper Functions of Part 2 ##########################
################################################################################


################################################################################


def day14p2():
    is_test = False
    data = get_input(parse1, test=is_test)

    total_time = 1000 if is_test else 2503

    points = collections.defaultdict(int)
    position = collections.defaultdict(int)
    state = collections.defaultdict(list)

    # Time: O(race_seconds * reindeers)
    # Mem: O(reindeers)
    for _ in range(total_time):
        # move one second
        for r in data:
            # calc dist for this second
            name, speed, run_t, wait_t = r
            if name not in state:
                state[name] = ["RUNNING", run_t]

            if state[name][0] == "WAITING":
                if state[name][1] <= 0:
                    state[name] = ["RUNNING", run_t]
                else:
                    state[name][1] -= 1
                    continue

            position[name] += speed

            state[name][1] -= 1

            if state[name][1] == 0:
                state[name] = ["WAITING", wait_t]

        max_ = max(list(position.values()))

        names = filter(lambda distance: distance[1] == max_, position.items())
        for name, _ in names:
            points[name] += 1

    print("Points:", points, "Position:", position)

    return max(map(lambda x: x[1], points.items()))


def main():
    divs = 40
    msg = 15
    n = (divs - msg) // 2
    divs += 1
    print()
    print("-" * (n), "Day 14 - Part 1", "-" * n)
    print("Result =>", day14p1())
    print()
    print("-" * (n), "Day 14 - Part 2", "-" * n)
    print("Result =>", day14p2())
    print()


main()
