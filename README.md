# advent-of-code

# Enviroment Variables

For being able to query the input data directly from AOC website, you'll need to:

- Create `.env` file
- Find the cookie that identifies you in the request Headers made to `https://adventofcode.com/<year>/day/<day>/input`
    - This header can be found using `DevTools` in Chrome or any other similar tool.
    - It is sent in the header at the param: `cookie`
- Put the cookie in the `.env` file with key `SESSION_COOKIE`

You are ready to start using this feature.

# Features / Usage

The features are:
- Run day script
- Create templates for days
- Create/initialize directory for AOC years
- Get the input data directly from AdventOfCode website and save into `.txt`

## Help

Command: `python3 aocUtils.py --help|-h`

## Run day

Command: `python3 aocUtils.py -r <day>` \
Optional Flag: `-y <year>` \
DefaultValue: `Current Year`

### Examples
```bash
$ python3 aocUtils.py -r 3
==> Running script: ./2020/day03.py


$ python3 aocUtils.py -r 3 -y 2017
==> Running script: ./2017/day03.py
```

## Initialize Year

Command: `python3 aocUtils.py -iy <year:optional>` \
DefaultValue: `Current Year`

Initialize year directory and create `yearutils.py`.

### Examples
```
$ python3 aocUtils.py -iy
==> Initializing year directory: ./2020
==> Creating dependency: ./2020/yearutils.py

$ python3 aocUtils.py -iy 2021
==> Initializing year directory: ./2021
==> Creating dependency: ./2021/yearutils.py
```


## Create template for day

Command: `python3 aocUtils.py --create-day|-cd <day>` \
Optional Flag: `-y <year>` \
DefaultValue: `Current Year`

Create template for day under `./<year>/` directory.

The year directory need to be initialized first, see [Initialize Year](#initialize-year).

This command will also query [https://adventofcode.com/](https://adventofcode.com/) for the data for the given day if the data is available.

### Examples
```
$ python3 aocUtils.py -cd 5
==> Creating day template: ./2020/day05.py

$ python3 aocUtils.py -cd 5 -y 2017
==> Creating day template: ./2017/day05.py
```

## Query Input Data

Command: `python3 aocUtils.py -i 7` \
Optional Flag: `-y <year>` \
DefaultValue: `Current Year`


Manual query of data. Folder of `year` need to exist or already be initialized. See [Initialize Year](#initialize-year). 

### Examples
```
$ python3 aocUtils.py python3 aocUtils.py -i 7
==> Get input data for year:2020 ✭ day:7
==> GET at https://adventofcode.com/2020/day/7/input
==> Success:  200
==> Creating Input files
==> Creating Input file: 2020/day07_input.txt
==> Creating Input file: 2020/day07_input_test.txt
```
