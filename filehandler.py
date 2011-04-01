import parser
from collections import namedtuple
import pickle

a_dict = {}
m_dict = {}
Movie = namedtuple('Movie', ['name', 'year'])
Actor = namedtuple('Actor', ['name'])

def pkl_check():
    try:
        f = open('adict.pkl')
        f.close()
        return True
    except IOError:
        return False

def load_pkl():
    adict_file = open('adict.pkl', 'rb')
    a_dict = pickle.load(adict_file)
    adict_file.close()
    mdict_file = open('mdict.pkl', 'rb')
    m_dict = pickle.load(mdict_file)
    mdict_file.close()

def store_pkl():
    adict_file = open('adict.pkl', 'wb')
    pickle.dump(a_dict, adict_file)
    adict_file.close()
    mdict_file = open('mdict.pkl', 'wb')
    pickle.dump(m_dict, mdict_file)
    mdict_file.close()

def fill_dicts():
    for actor_name, movies in parser.parse_actors(open('actors.list')):
        actor = Actor(actor_name)
        if actor not in a_dict:
            a_dict[actor] = []
        movie_tuples = [Movie(name, year) for name, year in movies]
        a_dict[actor].extend(movie_tuples)
        for movie in movie_tuples:
            if movie not in m_dict:
                m_dict[movie] = []
            m_dict[movie].append(actor)

def connected_actors(actor):
    movies = a_dict[actor]
    connected_set = set()
    for movie in movies:
        connected_set.update(m_dict[movie])
    connected_set.remove(actor)
    return list(connected_set)

def get_actor(name):
    if Actor(name) in a_dict:
        return Actor(name)
    else:
        raise KeyError

def link_actors(actor_name_1, actor_name_2):
    actor1 = Actor(actor_name_1)
    actor2 = Actor(actor_name_2)

    movie_set_1 = set(a_dict[actor1])
    movie_set_2 = set(a_dict[actor2])

    return list(movie_set_1 & movie_set_2)[0]
