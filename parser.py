#!/usr/bin/python

import re
MOVIE_RE = r'(?P<name>.*) (?P<year>\([\?\w/]{4,}\)).*'

def _parse_movie_line(line):
    tab_split = line.split('\t')
    info = tab_split[0]

    m = re.match(MOVIE_RE, info)
    name = None
    year = None
    if m:
        name = m.group('name')
        year_str = m.group('year')
        try:
            year = int(year_str[1:5])
        except ValueError:
            pass  # leave year as null
    return name, year

def parse_movies(input):
    has_started = False
    count = 0
    previous_movie = (None, None)
    for line in input:
        if has_started:
            name, year = _parse_movie_line(line)
            if name and (name, year) != previous_movie:
                yield name, year
                previous_movie = (name, year)
        else:
            if line.strip() == 'MOVIES LIST':
                has_started = True

if __name__ == '__main__':
    file = open('movies.list')
    for name, year in parse_movies(file):
        print name, str(year)
    file.close()

