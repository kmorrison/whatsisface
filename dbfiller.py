#!/usr/bin/python

import parser
import dbhandler

def write_movies():
    movie_filename = 'movies.list'
    movie_file = open(movie_filename)

    movies = parser.parse_movies(movie_file)
    dbhandler.persist_movies(movies)

if __name__ == '__main__':
    write_movies()
