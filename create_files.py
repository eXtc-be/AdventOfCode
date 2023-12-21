# create_files.py - creates today's subfolder and 2 python files for Advent of Code


import sys
from pathlib import Path
import requests
from requests.utils import cookiejar_from_dict

OVERWRITE = '{} already exists! Are you sure you want to overwrite it (y/N)? '
SESSION_COOKIE = 'session_cookie'
INPUT_URL = 'https://adventofcode.com/2023/day/{}/input'
INPUT_FILE = 'input'

day_number = None
year_number = 2023

if len(sys.argv) > 1:
    day_number = sys.argv[1]

if not day_number:
    day_number = input('Day number? ')

# create folder and file names
day_number = f'{int(day_number):02d}'
file_A = f'aoc_{str(year_number)}_{day_number}_A.py'
file_B = f'aoc_{str(year_number)}_{day_number}_B.py'

path = Path(day_number)

# check for existing folder and ask permission to delete/overwrite
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


if write:
    # create folder
    path.mkdir(parents=True, exist_ok=True)

    # create both files from template and replace certain placeholders
    for file, template in zip([file_A, file_B], ['template_A.py', 'template_B.py']):
        print(f'creating file {(path / file).absolute()}')
        with open(template, 'r') as in_file, open(path / file, 'w') as out_file:
            for line in in_file:
                if '<filename>' in line:
                    line = line.replace('<filename>', file)
                if '<year>' in line:
                    line = line.replace('<year>', str(year_number))
                if '<day>' in line:
                    line = line.replace('<day>', str(int(day_number)))
                if '<file_A>' in line:
                    line = line.replace('<file_A>', file_A[:-3])
                out_file.write(line)

    # download accompanying input file and save it to the folder
    with open(SESSION_COOKIE, 'r', encoding='utf-8') as cookie_file:
        cookie_data = cookie_file.read().strip()  # read session cookie data from file
        session_cookie = cookiejar_from_dict({'session': cookie_data})  # turn it into a cookie jar for use in session

    with requests.Session() as session:  # create session object
        input_url = INPUT_URL.format(int(day_number))
        print(f'downloading input file from {input_url}')
        session.cookies.update(session_cookie)  # set session cookie to 'authenticate'
        response = session.get(input_url)  # get the data from the remote server
        if response.status_code == 200:
            print(f'creating file {(path / INPUT_FILE).absolute()}')
            with open(path / INPUT_FILE, 'w') as out_file:
                out_file.write(response.content.decode('utf-8'))
        else:
            print(f'something went wrong, remote server returned status {response.status_code}')
