from src import database
from src.database import SessionLocal, engine
from sqlalchemy.sql import exists

import csv

database.Base.metadata.create_all(bind=engine)


def login(name: str, password: str) -> bool:
    """
    A function which facilitates login via the SQL database.
    :param name: The username associated with the user's account (max 30 characters).
    :param password: The password associated with the user's account (max 12 characters).
    :return: success: a boolean which determines whether the login was successful
    """
    db = SessionLocal()
    success = db.query(exists().where(database.User.name == name, database.User.password == password)).scalar()
    db.close()
    return success


def register(name: str, password: str) -> bool:
    """
    A function which facilitates login via the SQL database.
    :param name: A username (maximum 30 characters) that the user wants to register with
    :param password: A password (maximum 12 characters) that the user wants to register with
    :return: success: a boolean which determines whether registration was successful
    """
    db = SessionLocal()
    success = False
    # If a user with the specified username already exists, do not create a record.
    name_exists = db.query(exists().where(database.User.name == name)).scalar()
    if not name_exists:
        db_record = database.User(name=name, password=password, wins=0, losses=0, draws=0)
        db.add(db_record)
        db.commit()
        success = True

    db.close()
    return success


def read_cards_into_db():  # @staticmethod
    """
    Reads cards into the database.
    """
    db = SessionLocal()
    with open('sources/cards.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            # If a card exists, do not add to the db, skip it.
            card_exists = db.query(exists().where(database.Cards.name == row[0])).scalar()
            if not card_exists:
                db_record = database.Cards(name=row[0], card_type=row[1], attribute=row[2], monster_type=row[3],
                                           level=row[4], attack=row[5], defense=row[6], id=row[7], description=row[8])
                db.add(db_record)
                db.commit()
    db.close()
