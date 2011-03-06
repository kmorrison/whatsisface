
import ConfigParser
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    year = Column(Integer)

    def __init__(self, name, year):
        self.name = name
        self.year = year

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

def persist_movies(it):
    #get database
    mysql_db = engine_from_config('mysql')

    #get a db session
    Session = sessionmaker(bind=mysql_db)
    session = Session()

    for i, (name, year) in enumerate(it):
        movie = Movie(name, year)
        session.add(movie)

        #flush every 20000
        if i % 20000 == 0 and i > 0:
            session.commit()

    session.commit()
