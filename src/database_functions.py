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
    db_record = database.User(name=name, password=password, wins=0, losses=0, draws=0, decks="")
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
    result = {"error": "User not found", "name": "", "wins": -1, "losses": -1, "draws": -1}
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
                # If the card is a monster, get the necessary attributes and add into the database.
                if row[1] == "Monster":
                    create_monster_db_entry(row)
                else:  # row[1] == "Spell"
                    create_spell_db_entry(row)
    db.close()


def create_monster_db_entry(row: list[str]):
    """
    Helper function for read_cards_into_db. Creates a database entry for monster cards.
    :param row: a string list representing a row from the cards.csv file.
    :return:
    """
    db = SessionLocal()
    db_record = database.Cards(name=row[0], card_type=row[1], attribute=row[2], monster_type=row[3],
                               level=row[4], attack=row[5], defense=row[6], description=row[7])
    db.add(db_record)
    db.commit()
    db.close()


def create_spell_db_entry(row: list[str]):
    """
        Helper function for read_cards_into_db. Creates a database entry for spell cards.
        :param row: a string list representing a row from the cards.csv file.
        :return:
        """
    db = SessionLocal()
    if len(row) == 5:  # No effect args.
        db_record = database.Cards(name=row[0], card_type=row[1], icon=row[2],
                                   description=row[3], spell_effect=row[4])
        db.add(db_record)
        db.commit()
    else:  # Compile all effect args into a single comma-separated string.
        num_args = len(row) - 5
        spell_effect_args = ""
        for i in range(num_args-1):
            spell_effect_args += row[5+i]
            spell_effect_args += ","
        spell_effect_args += row[4+num_args]
        db_record = database.Cards(name=row[0], card_type=row[1], icon=row[2],
                                   description=row[3], spell_effect=row[4], spell_effect_args=spell_effect_args)
        db.add(db_record)
        db.commit()


def get_card_info(name: str) -> list:
    """
    Reads a card from the database and returns a list of the available parameters.
    :param name: A string containing the name of the card.
    :return: A list of parameters of the card.
    """
    db = SessionLocal()
    existing = db.query(exists().where(database.Cards.name == name)).scalar()
    card_info = []
    if existing:
        card = db.query(database.Cards).filter(database.Cards.name == name).one()
        db.close()
        if card.card_type == "Monster":
            card_info = [card.name, card.description, card.attribute, card.monster_type,
                         card.level, card.attack, card.defense]
        else:
            effect_args = []
            if card.spell_effect_args is not None:
                effect_args = card.spell_effect_args.split(",")
            card_info = [card.name, card.icon, card.description, card.spell_effect]
            card_info = card_info + effect_args
    return card_info


def get_deck_from_db(name: str, index: int) -> list:
    """
    Gets one of the user's decks from the database.
    :param name: A string containing the user's name.
    :param index: an integer containing the index of the deck.
    :return: deck: a list containing the user's deck (names of every card)
    """
    db = SessionLocal()
    deck = []
    if user_exists(name):
        user = db.query(database.User).filter(database.User.name == name).one()
        deckstring = user.decks
        decks = deckstring.split("*")
        if index < len(decks):
            deck = decks[index].split("#")
    db.close()
    return deck


def print_user_decks(name: str):
    """
    prints all decks for a specified user.
    :param name: A string containing the user's name.
    :return:
    """
    db = SessionLocal()
    if user_exists(name):
        user = db.query(database.User).filter(database.User.name == name).one()
        deckstring = user.decks
        decks = deckstring.split("*")
        for deck in decks:
            print(deck.split("#"))


def save_user_deck(name: str, deck: list):
    """
    Saves the user's deck into the database.
    :param name: The name of the user who is saving their deck.
    :param deck: A list containing the names of the cards in the deck.
    :return:
    """
    db = SessionLocal()
    deckstring = ""
    if user_exists(name) and len(deck) != 0:
        for i in range(len(deck) - 1):
            deckstring += deck[i] + "#"
        deckstring += deck[len(deck) - 1]
        user = db.query(database.User).filter(database.User.name == name).one()
        if len(user.decks) == 0:
            user.decks += deckstring
        else:
            user.decks = user.decks + "*" + deckstring
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
