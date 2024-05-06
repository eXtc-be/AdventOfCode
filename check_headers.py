# check_headers.py - checks whether the header matches the filename in all aoc files


import sys
from pathlib import Path
import re

FILENAME = re.compile(r'(?:aoc_\d{4}_\d{2}_[A-Z]{1,2}(?:_extern)?_\d[a-z]?|extern_\d[a-z]?)\.py')

path_parts = ['.']

if len(sys.argv) > 1:
    path_parts.append(sys.argv[1])

if len(sys.argv) > 2:
    path_parts.append(f'{int(sys.argv[2]):02d}')

for file in Path('/'.join(path_parts)).glob('**/*.py'):
    # only look at paths that have 3 parts and start with 4 numbers (i.e. years)
    if len(file.parts) == 3 and len(file.parts[0]) == 4 and file.parts[0].isdigit():
        first_line = ''

        print(file)

        year, day, filename = file.parts

        if FILENAME.match(filename):
            if len(filename.split('_')) > 2:
                if filename.split('_')[1] != year:
                    print('\tFile appears to be for the wrong year')
                if filename.split('_')[2] != day:
                    print('\tFile appears to be for the wrong day')
        else:
            print('\tFilename does not conform to expected format')

        with file.open('r', encoding='utf-8') as f:
            first_line = f.readline().strip()

        if FILENAME.match(filename):
            if filename.startswith('aoc'):
                if first_line.startswith('#'):
                    if len(first_line.split()) > 3:
                        if first_line.split()[1] == filename:
                            if int(filename.split('_')[2]) != int(first_line.split()[4][:-1]):
                                print('\tDay number does not match')
                            if filename.split('_')[3] == 'AB':
                                if first_line.split()[-5:] != 'part 1 + part 2'.split():
                                    print('\tPart number does not match')
                            elif 'AB'.index(filename.split('_')[3]) + 1 != int(first_line.split()[-1]):
                                print('\tPart number does not match')
                        else:
                            print('\tFirst line does not start with the filename')
                    else:
                        print('\tFirst line does not conform to expected format')
                else:
                    print('\tFirst line is not a comment')

        print('-' * 100)
