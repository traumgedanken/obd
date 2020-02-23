from sqlalchemy import Column, Integer, String, DateTime, \
    Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

db_str = 'postgres://admin:admin@localhost:5432/kpi'
db = create_engine(db_str)
Base = declarative_base()


class Game(Base):
    __tablename__ = 'game'
    __columns__ = ('id', 'ticket_sold', 'sport_type', 'date')

    id = Column(Integer, primary_key=True)
    ticket_sold = Column(Integer)
    sport_type = Column(String)
    date = Column(DateTime)

    scores = relationship('Score')
    events = relationship('Event')

    def __init__(self, ticket_sold=None, sport_type=None, date=None):
        self.ticket_sold = ticket_sold
        self.sport_type = sport_type
        self.date = date


class Stadium(Base):
    __tablename__ = 'stadium'
    __columns__ = ('id', 'country', 'seats', 'has_cover')

    id = Column(Integer, primary_key=True)
    country = Column(String)
    seats = Column(Integer)
    has_cover = Column(Boolean)

    events = relationship('Event')

    def __init__(self, country=None, seats=None, has_cover=None):
        self.country = country
        self.seats = seats
        self.has_cover = has_cover


class Team(Base):
    __tablename__ = 'team'
    __columns__ = ('id', 'price', 'country', 'name')

    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    country = Column(String)
    name = Column(String)

    scores = relationship('Score')

    def __init__(self, price=None, country=None, name=None):
        self.price = price
        self.country = country
        self.name = name


class Score(Base):
    __tablename__ = 'score'
    __columns__ = ('points', 'game_id', 'team_id')

    points = Column(Integer)
    game_id = Column(Integer, ForeignKey('game.id'), primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'), primary_key=True)

    def __init__(self, points, game_id=None, team_id=None):
        self.points = points
        self.game_id = game_id
        self.team_id = team_id


class Event(Base):
    __tablename__ = 'event'
    __columns__ = ('game_id', 'stadium_id')

    game_id = Column(Integer, ForeignKey('game.id'), primary_key=True)
    stadium_id = Column(Integer, ForeignKey('stadium.id'), primary_key=True)

    def __init__(self, game_id=None, stadium_id=None):
        self.game_id = game_id
        self.stadium_id = stadium_id


session = sessionmaker(db)()
Base.metadata.create_all(db)

MODELS = {
    'game': Game, 'team': Team, 'stadium': Stadium,
    'event': Event, 'score': Score
};
TABLES = dict((tname, MODELS[tname].__columns__) for tname in MODELS)


def insert(tname, opts):
    object_class = MODELS[tname]
    obj = object_class(**opts)
    session.add(obj)


def get(tname, opts=None):
    objects_class = MODELS[tname]
    objects = session.query(objects_class)
    for key, item in opts.items():
        objects = objects.filter(getattr(objects_class, key) == item)

    return list(objects)


def update(tname, condition, opts):
    column, value = condition
    object_class = MODELS[tname]
    filter_attr = getattr(object_class, column)
    objects = session.query(object_class).filter(filter_attr == value)

    for obj in objects:
        for key, item in opts.items():
            setattr(obj, key, item)


def delete(tname, opts):
    objects_class = MODELS[tname]
    objects = session.query(objects_class)
    for key, item in opts.items():
        objects = objects.filter(getattr(objects_class, key) == item)

    objects.delete()


def create_random_teams():
    with open('scripts/random.sql', 'r') as file:
        sql = file.read()
        session.execute(sql)


def commit():
    session.commit()