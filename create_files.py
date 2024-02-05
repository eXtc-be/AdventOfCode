# create_files.py - creates today's subfolder and 2 python files for Advent of Code,
# downloads input file and html and saves them
# extracts today's title and description and inserts them into the templates


import sys
from pathlib import Path
import requests
from requests.utils import cookiejar_from_dict
from shutil import rmtree
import re

OVERWRITE = '{} already exists! Are you sure you want to overwrite it (y/N)? '
SESSION_COOKIE = 'session_cookie'
HTML_URL = 'https://adventofcode.com/{}/day/{}'
HTML_FILE = '{}_{}.html'
INPUT_URL = 'https://adventofcode.com/{}/day/{}/input'
INPUT_FILE = 'input_{}_{}'
TEMPLATE_FILE = 'template_{}.txt'
OUTPUT_FILE = 'aoc_{}_{}_{}_1.py'

day_string = None
year_string = None

if len(sys.argv) > 1:
    year_string = sys.argv[1]

if len(sys.argv) > 2:
    day_string = sys.argv[2]

if not year_string:
    while True:
        year_string = input('Year number? ')
        if year_string.isdigit() and len(year_string) == 4 and 1970 <= int(year_string) <= 2100:
            break

if not day_string:
    while True:
        day_string = input('Day number? ')
        if day_string.isdigit() and 0 < len(day_string) <= 2 and 1 <= int(day_string) <= 12:
            break

# create folder name and Path
day_string = f'{int(day_string):02d}'
path = Path(year_string) / Path(day_string)

# check for existing folder and ask permission to delete/overwrite
write = False
if path.exists():
    if input(OVERWRITE.format(path)).lower().startswith('y'):
        write = True
        print(f'removing folder {path.absolute()} and all of its contents')
        rmtree(path)
else:
    write = True


if write:
    # create folder
    path.mkdir(parents=True, exist_ok=True)

    # open the cookie file and store its contents in a variable for later use
    with open(SESSION_COOKIE, 'r', encoding='utf-8') as cookie_file:
        cookie_data = cookie_file.read().strip()  # read session cookie data from file
        session_cookie = cookiejar_from_dict({'session': cookie_data})  # turn it into a cookie jar for use in session

    input_url = INPUT_URL.format(int(year_string), int(day_string))
    html_url = HTML_URL.format(int(year_string), int(day_string))

    title = ''  # make sure title is accessible outside with-block
    description = ''  # make sure description is accessible outside with-block

    # download today's description and input files
    with requests.Session() as session:  # create session object
        session.cookies.update(session_cookie)  # set session cookie to 'authenticate'

        print(f'downloading description from {html_url}')
        response = session.get(html_url)  # get the data from the remote server
        if response.status_code == 200:
            html = response.text
            html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)  # remove html comments
            html = re.sub(r'<script>.*?</script>', '', html, flags=re.DOTALL)  # remove java script

            # extract today's title and description
            # first get everything between <article> and </article>
            art_match = re.search(r'<article.*?>(.*?)</article>', html, flags=re.DOTALL)
            if art_match:
                article = art_match.group(1)

                # extract title from article
                title_match = re.match(r'<h2>--- Day \d\d?: (.*?) ---</h2>', article)
                if title_match:
                    title = title_match.group(1)

                # extract description from article (it's the last paragraph)
                para_match = re.findall(r'<p>(.*?)</p>', article)
                if para_match:
                    description = para_match[-1]
                    description = re.sub(r'<.+?>', '', description, flags=re.DOTALL)  # remove any html tags

            # save html to a file
            html_file = HTML_FILE.format(year_string, day_string)
            print(f'creating html file {(path / html_file).absolute()}')
            with open(path / html_file, 'w', encoding='utf-8') as out_file:
                out_file.write(html)
        else:
            print(f'something went wrong, remote server returned status {response.status_code}')
            # exit()

        print(f'downloading input file from {input_url}')
        response = session.get(input_url)  # get the data from the remote server
        if response.status_code == 200:
            input_file = INPUT_FILE.format(year_string, day_string)
            print(f'creating input file {(path / input_file).absolute()}')
            with open(path / input_file, 'w', encoding='utf-8') as out_file:
                out_file.write(response.text)
        else:
            print(f'something went wrong, remote server returned status {response.status_code}')
            # exit()

    # create both files from template and replace placeholders
    file_A = ''
    for letter in 'AB':
        output_file = OUTPUT_FILE.format(str(year_string), day_string, letter)
        template = TEMPLATE_FILE.format(letter)

        if letter == 'A':
            file_A = output_file  # remember name of first script so we can import from it in the next one(s)

        print(f'creating output file {(path / output_file).absolute()}')
        with open(template, 'r', encoding='utf-8') as in_file, open(path / output_file, 'w', encoding='utf-8') as out_file:
            for line in in_file:
                if '<filename>' in line:
                    line = line.replace('<filename>', output_file)
                if '<day>' in line:
                    line = line.replace('<day>', str(int(day_string)))
                if '<title>' in line:
                    line = line.replace('<title>', title)
                if '<description>' in line:
                    line = line.replace('<description>', description)
                if '<url>' in line:
                    line = line.replace('<url>', html_url)
                if '<year>' in line:
                    line = line.replace('<year>', str(year_string))
                if '<0_day>' in line:
                    line = line.replace('<0_day>', day_string)
                if '<file_A>' in line:  # from <file_A> import
                    line = line.replace('<file_A>', file_A[:-3])  # cut '.py.
                out_file.write(line)
