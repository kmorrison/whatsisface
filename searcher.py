#!/usr/bin/python


from filehandler import Movie, Actor, connected_actors, get_actor
from collections import deque
from itertools import tee, izip
import filehandler

def commify_name(name):
    if len(name.split(',')) == 1:
        white_split = name.split()
        size = len(white_split)
        return white_split[-1] + ', ' + ' '.join(white_split[:size-1])
    else:
        return name

def reverse_path(src, sink, path_dict):
    path = [sink]
    while True:
        new_node = path_dict[path[-1]]
        path.append(new_node)
        if new_node == src:
            break
    return path[::-1]

def bfs(name1, name2):
    print 'filling dictionaries'
    filehandler.fill_dicts()
    print 'performing bfs'
    actor1 = get_actor(name1)
    actor2 = get_actor(name2)

    previous_paths = {}
    open_q = deque()

    open_q.appendleft(actor1)
    total_added = 0
    iters = 0
    depth = 0
    while open_q:
        actor = open_q.pop()

        if actor.name == actor2.name:
            print 'found solution...'
            path = reverse_path(actor1.name, actor2.name, previous_paths)
            return path

        new_actors = connected_actors(actor)
        actors_not_seen = [ac for ac in new_actors if ac.name not in previous_paths]
        total_added += len(actors_not_seen)
        for ac in actors_not_seen:
            previous_paths[ac.name] = actor.name
            open_q.appendleft(ac)

        iters += 1
        size = total_added - iters

    assert False

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def search(n1, n2):
    name1 = commify_name(n1)
    name2 = commify_name(n2)

    path = bfs(name1, name2)
    for a1, a2 in pairwise(path):
        print a1, a2
        common_movie = filehandler.link_actors(a1, a2)
        print common_movie
    return path

if __name__ == '__main__':
    path = search('Matt Damon', 'Jon Hamm')





