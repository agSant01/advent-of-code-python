import re

import yearutils as yu


def parse(line: str):
    items = line.split()
    val = dict([item.split(":") for item in items])
    return val


def day4p1():
    passports = yu.get_input("day04_input.txt", parse)
    valid = 0
    curr_p = {}
    for p in passports:
        if p:
            curr_p.update(p)
        else:
            k = len(curr_p.keys())
            if curr_p.get("cid"):
                k -= 1
            if k == 7:
                valid += 1
            curr_p.clear()
    return valid


# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.


ecl_m = re.compile(r"#[0-9a-f]{6,6}")
pid_m = re.compile(r"[0-9]{9,9}")


def isValidPassport(p):
    if not (1920 <= int(p["byr"]) <= 2020):
        return False

    if not (2010 <= int(p["iyr"]) <= 2020):
        return False

    if not (2020 <= int(p["eyr"]) <= 2030):
        return False

    if not (p["hgt"].endswith(("cm", "in")) and p["hgt"][:-2].isnumeric()):
        return False

    if p["hgt"].endswith("cm"):
        if not (150 <= int(p["hgt"][:-2]) <= 193):
            return False

    # If in, the number must be at least 59 and at most 76.
    if p["hgt"].endswith("in"):
        if not (59 <= int(p["hgt"][:-2]) <= 76):
            return False

    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    if not ecl_m.fullmatch(p["hcl"]):
        return False

    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    if p["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False

    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    if not pid_m.fullmatch(p["pid"]):
        return False

    return True


def day4p2():
    passports = yu.get_input("day04_input.txt", parse)
    valid = 0
    curr_p = {}
    for p in passports:
        if p:
            curr_p.update(p)
        else:
            k = len(curr_p.keys())
            if curr_p.get("cid"):
                k -= 1
            if k == 7 and isValidPassport(curr_p):
                valid += 1
            curr_p.clear()
    return valid


def main():
    print("Day 04 - Part 1")
    print(day4p1())

    print("Day 04 - Part 2")
    print(day4p2())


main()
