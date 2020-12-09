import utils as ut


def parse(line):
    s = set()
    for char in line:
        s.add(char)
    return s


def day06p1():
    persons = ut.get_input("day06_input.txt", parse)

    total_sum = 0
    group_answers = set()
    for person in persons:
        if person:
            group_answers.update(person)
        else:
            # empty line, end of group
            total_sum += len(group_answers)
            group_answers.clear()

    return total_sum


def day06p2():
    persons = ut.get_input("day06_input.txt", parse)

    total_sum = 0

    group_answers = set()
    new_group = True
    for person in persons:
        if new_group:
            group_answers.update(person)
            new_group = False

        if person:
            group_answers.intersection_update(person)
        else:
            # empty line, end of group
            new_group = True
            total_sum += len(group_answers)
            group_answers.clear()

    return total_sum


def main():
    print("Day 06 - Part 1")
    print(day06p1())

    print("Day 06 - Part 2")
    print(day06p2())


main()
