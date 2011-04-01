
import logging
import ConfigParser
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

ERROR_LOG_NAME = 'dberror.log'
logging.basicConfig(filename=ERROR_LOG_NAME, level=logging.DEBUG)

Base = declarative_base()

actors_movies = Table('actors_movies', Base.metadata,
    Column('actor_id', Integer, ForeignKey('actors.id')),
    Column('movie_id', Integer, ForeignKey('movies.id'))
    )

class Movie(Base):
    """Note: manually created index on movie.name, makes seeding the
    database run way faster. If slow, make sure you check that index was
    created"""
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), index=True)
    year = Column(Integer)

    def __init__(self, name, year):
        self.name = name
        self.year = year

class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    movies = relationship('Movie', secondary=actors_movies, backref='actors')

    def __init__(self, name):
        self.name = name

def engine_from_config(config_section):
    config = ConfigParser.ConfigParser()
    config.read('database.cfg')

    #extract from config
    db_type = config.get(config_section, 'db_type')
    user = config.get(config_section, 'user')
    location = config.get(config_section, 'location')
    password = config.get(config_section, 'password')
    port = config.get(config_section, 'port')
    db_name = config.get(config_section, 'db_name')

    #build engine url
    engine_url = ('{0}://{1}:{2}@{3}:{4}/{5}'
                 .format(db_type, user, password, location, port, db_name))

    engine = create_engine(engine_url)

    #create tables if necessary
    metadata = Base.metadata
    metadata.create_all(engine)
    return engine
    
class QueryHandler():

    def __init__(self, config_section):
        db_engine = engine_from_config(config_section)
        Session = sessionmaker(bind=db_engine)
        self.session = Session()

    def connected_actors(self, actor):
        movies = actor.movies
        connected_actors = {}
        for movie in movies:
            movie_actors = movie.actors
            for movie_actor in movie_actors:
                connected_actors[movie_actor.name] = movie_actor
        return connected_actors.values()

    def get_actor(self, actor_name):
        return self.session.query(Actor).filter(Actor.name==actor_name).one()

def persist_movies(it):
    #get database
    mysql_db = engine_from_config('mysql')

    #get a db session
    Session = sessionmaker(bind=mysql_db)
    session = Session()

    for i, (name, year) in enumerate(it):
        if not year:
            logging.warning('ERROR: no year for {0}'.format(name))

        movie = Movie(name, year)
        session.add(movie)

        #flush every 20000
        if i % 20000 == 0 and i > 0:
            session.commit()

    session.commit()

def persist_actors(it):
    mysql_db = engine_from_config('mysql')

    #get a db session
    Session = sessionmaker(bind=mysql_db)
    session = Session()

    for i, (actor_name, actors_movies) in enumerate(it):
        if not actors_movies:
            logging.warning('ERROR: actor {0}, {1}'.format(i, actor_name))
            continue

        movie_names, movie_years = zip(*actors_movies)
        movies = session.query(Movie).filter(Movie.name.in_(movie_names)).all()
        if not movies:
            logging.error('no movies returned for ' + actor_name)
            continue

        movie_lookup = set(actors_movies)
        movies = [movie for movie in movies 
                 if (movie.name, movie.year) in movie_lookup]
        actor = Actor(actor_name)
        actor.movies = movies

        session.add(actor)

        #flush every 20000
        if i % 20000 == 0 and i > 0:
            session.commit()

    session.commit()
