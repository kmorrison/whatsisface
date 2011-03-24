#!/usr/bin/python

import re
from pprint import pprint
MOVIE_RE = r'(?P<name>.*) (?P<year>\([\?\d/IVXL]{4,}\)).*'

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
    input.close()

def parse_actors(input):
    has_started = False
    previous_movie = (None, None)
    current_actor = None
    current_actors_movies = []
    for line in input:
        if has_started:
            if not line.strip() and current_actor:
                yield current_actor, current_actors_movies
                current_actor = None
                current_actors_movies = []
            else:
                tabline = line.split('\t')
                actor = tabline[0]
                if actor and len(tabline) > 1:
                    current_actor = actor
                movie_info = tabline[-1].strip()
                name, year = _parse_movie_line(movie_info)
                if name and (name, year) != previous_movie:
                    current_actors_movies.append((name, year))
                    previous_movie = (name, year)
        else:
            if line.strip() == 'THE ACTORS LIST':
                has_started = True
    input.close()

if __name__ == '__main__':
    file = open('movies.list')
    file.close()
