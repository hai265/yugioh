from src import database
from src.database import SessionLocal, engine
from sqlalchemy.sql import exists

import csv

database.Base.metadata.create_all(bind=engine)


def login(name: str, password: str) -> dict:
    """
    A function which facilitates login via the SQL database.
    Args:
        name: The username associated with the user's account (max 20 characters).
        password: The password associated with the user's account (max 12 characters).
    Returns: a dict containing the user's statistics.
    """
    print("name: " + name + ", password: " + password)
    db = SessionLocal()
    success = db.query(exists().where(database.User.name == name).where(database.User.password == password)).scalar()
    if success:
        stats = get_user_stats(name)
    else:  # Will reach this if the password is incorrect.
        stats = {"name": "", "wins": -1, "losses": -1, "draws": -1}
    db.close()

    return stats


def register(name: str, password: str) -> dict:
    """
    A function which facilitates login via the SQL database.
    Args:
        name: A username (maximum 20 characters) that the user wants to register with
        password: A password (maximum 12 characters) that the user wants to register with
    Returns: a boolean which determines whether registration was successful
    """
    db = SessionLocal()
    db_record = database.User(name=name, password=password, wins=0, losses=0, draws=0)
    db.add(db_record)
    db.commit()
    db.close()
    return get_user_stats(name)


def user_exists(name: str) -> bool:
    """
    Checks if a user with the specified name exists in the database.
    :param name: a string containing the username which will be checked
    :return: existing: a boolean which states whether the user exists.
    """

    db = SessionLocal()
    existing = db.query(exists().where(database.User.name == name)).scalar()
    db.close()
    return existing


def get_user_stats(name: str) -> dict:
    """
    Gets the win/loss/draw statistics for the specified user.
    :param name: a string containing the name of the user.
    :return: result: a dict containing a string entry for username and three integer entries for wins, losses, and draws
             e.g. {"Yugi", 27, 1, 0}
    """
    result = {"name": "", "wins": -1, "losses": -1, "draws": -1}
    db = SessionLocal()
    if user_exists(name):
        query = db.query(database.User).filter(database.User.name == name).one()
        result = {"name": query.name, "wins": query.wins, "losses": query.losses, "draws": query.draws}
    db.close()

    return result


def read_cards_into_db():  # @staticmethod
    """
    Reads cards from the file cards.csv into the Cards table.
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


def update_win_loss_draw(name: str, status: str):
    """
    Updates the win/loss/draw statistic for a specified user.
    :param name: A string containing the name of the user.
    :param status: A one-character string containing "w", "l", or "d" to specify a win, loss, or draw.
    :return:
    """
    db = SessionLocal()
    query = db.query(database.User).filter(database.User.name == name).one()
    if status == "w":
        query.wins += 1
    elif status == "l":
        query.losses += 1
    elif status == "d":
        query.draws += 1
    db.commit()
    db.close()
