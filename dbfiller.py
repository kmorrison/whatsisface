#!/usr/bin/python

from optparse import OptionParser

import parser
import dbhandler

def write_movies():
    movie_file = open('movies.list')
    dbhandler.persist_movies(parser.parse_movies(movie_file))

def write_actors():
    actor_file = open('actors.list')
    dbhandler.persist_actors(parser.parse_actors(actor_file))

TABLE_METHODS = {'movies': write_movies, 'actors': write_actors}
if __name__ == '__main__':
    opt_parser = OptionParser(usage='usage: %prog write-table')
    opt_parser.add_option('-t', '--table',
                    action='store',
                    choices=list(TABLE_METHODS.keys()),
                    help='name of table to fill')
    options, args = opt_parser.parse_args()
    write_method = TABLE_METHODS[options.table]
    write_method()
