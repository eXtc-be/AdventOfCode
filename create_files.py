# create_files.py - creates a subfolder and 2 python files for day of advent of code


import sys
import os
from pathlib import Path


OVERWRITE = '{} already exists! Are you sure you want to overwrite it (y/N)? '

day_number = None

if len(sys.argv) > 1:
    day_number = sys.argv[1]

if not day_number:
    day_number = input('Day number? ')

day_number = f'{int(day_number):02d}'
file_A = f'aoc_{day_number}_A.py'
file_B = f'aoc_{day_number}_B.py'

path = Path(day_number)

write = False
if path.exists():
    if input(OVERWRITE.format(path)).lower().startswith('y'):
        write = True
        for file in path.glob('*.*'):
            print(f'removing file {file.absolute()}')
            file.unlink()
        path.rmdir()
else:
    write = True

path.mkdir(parents=True, exist_ok=True)

if write:
    for file,template in zip([file_A, file_B], ['template_A.py', 'template_B.py']):
        print(f'creating file {(path / file).absolute()}')
        with open(template, 'r') as in_file, open(path / file, 'w') as out_file:
            for line in in_file:
                if '<filename>' in line:
                    line = line.replace('<filename>', file)
                if '<day>' in line:
                    line = line.replace('<day>', str(int(day_number)))
                if '<file_A>' in line:
                    line = line.replace('<file_A>', file_A[:-3])
                out_file.write(line)
