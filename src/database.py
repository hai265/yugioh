from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

""" Adapted from 
https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-
interact-with-databases-in-a-flask-application#step-1-installing-flask-and-flask-sqlalchemy
and https://docs.sqlalchemy.org/en/14/index.html
"""

Base = declarative_base()
DATABASE_URI = "mysql+pymysql://root:$MYSQL_ROOT_PASSWORD@mysql/$MYSQL_DATABASE"
# "sqlite:///./test_database.db"
# "mysql+pymysql://root:$upr3me1@localhost/yugioh_test"
# MILESTONE DB: "mysql+pymysql://admin:$upr3meK1ng@dbinstance-1.c9lngznprt4c.us-east-1.rds.amazonaws.com:3306/yugiohdb"


engine = create_engine(DATABASE_URI)

connection = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    """
    Relational database for users of the game.
    """
    __tablename__ = "Users"

    name = Column(String(30), primary_key=True, nullable=False)
    password = Column(String(12), nullable=False)
    wins = Column(Integer)
    losses = Column(Integer)
    draws = Column(Integer)

    def __repr__(self):
        return f'<User {self.name}>'


class Cards(Base):
    __tablename__ = "Cards"
    name = Column(String(52), primary_key=True, nullable=False)
    card_type = Column(String(7), nullable=False)
    attribute = Column(String(6), nullable=False)
    monster_type = Column(String(13),  nullable=False)
    level = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    id = Column(Integer, nullable=False)
    description = Column(String(800), nullable=False)
