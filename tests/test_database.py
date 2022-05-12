import unittest
from src.database import SessionLocal
from src.database import Cards
from src.database import User
from src.database import engine
from src.database_functions import register, login, get_user_stats, user_exists, update_win_loss_draw
from src.database_functions import save_user_deck, read_cards_into_db, get_deck_from_db, get_card_info, print_user_decks
from sqlalchemy import select


class TestReadCards(unittest.TestCase):
    def test_read_cards_nominal(self):
        read_cards_into_db()
        db = SessionLocal()
        db_record = db.scalars(select(Cards)).first()
        self.assertEqual("Monster", db_record.card_type)
        stmt = Cards.__table__.delete().where(Cards.name != "")
        engine.execute(stmt)
        db.close()


class TestRegister(unittest.TestCase):
    def test_register_nominal(self):
        db = SessionLocal()
        name = "Yugi"
        password = "kingofgames"
        result = register(name, password)
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        db.close()
        self.assertEqual(result["name"], "Yugi")  # add assertion here
        self.assertEqual(result["wins"], 0)
        self.assertEqual(result["losses"], 0)
        self.assertEqual(result["draws"], 0)


class TestLogin(unittest.TestCase):
    def test_login_nominal(self):
        db = SessionLocal()
        name = "Yugi"
        password = "kingofgames"
        db_record = User(name=name, password=password, wins=34, losses=5, draws=1, decks="")
        db.add(db_record)
        db.commit()
        result = login(name, password)
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        db.close()
        self.assertEqual(result["name"], "Yugi")  # add assertion here
        self.assertEqual(result["wins"], 34)
        self.assertEqual(result["losses"], 5)
        self.assertEqual(result["draws"], 1)

    def test_login_nonexistent_user(self):
        db = SessionLocal()
        name = "Yugi"
        password = "kingofgames"
        result = login(name, password)
        db.close()
        self.assertEqual(result["name"], "")  # add assertion here
        self.assertEqual(result["wins"], -1)
        self.assertEqual(result["losses"], -1)
        self.assertEqual(result["draws"], -1)


class TestGetUserStats(unittest.TestCase):

    def test_get_nominal(self):
        db = SessionLocal()
        name = "Yugi"
        password = "kingofgames"
        db_record = User(name=name, password=password, wins=34, losses=5, draws=1)
        db.add(db_record)
        db.commit()
        user_stats = get_user_stats(name)
        self.assertEqual("Yugi", user_stats["name"])
        self.assertEqual(34, user_stats["wins"])
        self.assertEqual(5, user_stats["losses"])
        self.assertEqual(1, user_stats["draws"])
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        db.close()

    def test_get_nonexistent(self):
        db = SessionLocal()
        name = "Yugi"
        user_stats = get_user_stats(name)
        self.assertEqual("", user_stats["name"])
        self.assertEqual(-1, user_stats["wins"])
        self.assertEqual(-1, user_stats["losses"])
        self.assertEqual(-1, user_stats["draws"])
        db.close()


class TestUserExists(unittest.TestCase):
    def test_user_exists_true(self):
        db = SessionLocal()
        name = "Yugi"
        password = "kingofgames"
        db_record = User(name=name, password=password, wins=34, losses=5, draws=1)
        db.add(db_record)
        db.commit()
        self.assertEqual(True, user_exists(name))
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        db.close()

    def test_user_exists_false(self):
        db = SessionLocal()
        name = "Yugi"
        self.assertEqual(False, user_exists(name))
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        db.close()


class TestUpdateWinLossDraw(unittest.TestCase):
    def test_update_win(self):
        db = SessionLocal()
        name = "Yugi"
        password = "kingofgames"
        db_record = User(name=name, password=password, wins=0, losses=0, draws=0)
        db.add(db_record)
        db.commit()
        update_win_loss_draw(name, "w")
        user = db.query(User).filter(User.name == name).one()
        self.assertEqual(1, user.wins)
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        db.close()

    def test_update_loss(self):
        db = SessionLocal()
        name = "Yugi"
        password = "kingofgames"
        db_record = User(name=name, password=password, wins=0, losses=0, draws=0, decks="")
        db.add(db_record)
        db.commit()
        update_win_loss_draw(name, "l")
        user = db.query(User).filter(User.name == name).one()
        self.assertEqual(1, user.losses)
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        db.close()

    def test_update_draw(self):
        db = SessionLocal()
        name = "Yugi"
        password = "kingofgames"
        db_record = User(name=name, password=password, wins=0, losses=0, draws=0, decks="")
        db.add(db_record)
        db.commit()
        update_win_loss_draw(name, "d")
        user = db.query(User).filter(User.name == name).one()
        self.assertEqual(1, user.draws)
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        db.close()

    def test_update_invalid_char(self):
        db = SessionLocal()
        name = "Yugi"
        password = "kingofgames"
        db_record = User(name=name, password=password, wins=0, losses=0, draws=0, decks="")
        db.add(db_record)
        db.commit()
        update_win_loss_draw(name, "e")
        user = db.query(User).filter(User.name == name).one()
        self.assertEqual(0, user.wins)
        self.assertEqual(0, user.losses)
        self.assertEqual(0, user.draws)
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        db.close()


class TestSaveUserDeck(unittest.TestCase):
    # This function is only run after a user has logged in. Therefore the user will exist in the db.
    def test_save_user_deck_nominal(self):
        db = SessionLocal()
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        name = "Yugi"
        password = "kingofgames"
        deck = ["Mammoth Graveyard", "Summoned Skill", "Dark Magician Girl"]
        deckstring = "Mammoth Graveyard#Summoned Skill#Dark Magician Girl"
        db_record = User(name=name, password=password, wins=0, losses=0, draws=0, decks="")
        db.add(db_record)
        db.commit()
        save_user_deck("Yugi", deck)
        user = db.query(User).filter(User.name == name).one()
        self.assertEqual(deckstring, user.decks)
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        db.close()

    def test_save_user_deck_empty(self):
        db = SessionLocal()
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        name = "Yugi"
        password = "kingofgames"
        deck = []
        db_record = User(name=name, password=password, wins=0, losses=0, draws=0, decks="")
        db.add(db_record)
        db.commit()
        save_user_deck("Yugi", deck)
        user = db.query(User).filter(User.name == name).one()
        self.assertEqual(0, len(user.decks))
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        db.close()

    def test_save_user_deck_two_decks(self):
        db = SessionLocal()
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        name = "Yugi"
        password = "kingofgames"
        deck2 = ["Dark Magician", "Gaia The Fierce Knight", "Black Luster Soldier"]
        deckstring1 = "Mammoth Graveyard#Summoned Skill#Dark Magician Girl"
        deckstring2 = "Dark Magician#Gaia The Fierce Knight#Black Luster Soldier"
        db_record = User(name=name, password=password, wins=0, losses=0, draws=0, decks=deckstring1)
        db.add(db_record)
        db.commit()
        save_user_deck("Yugi", deck2)
        user = db.query(User).filter(User.name == name).one()
        decklist = deckstring1 + "*" + deckstring2
        self.assertEqual(decklist, user.decks)
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        db.close()


class TestGetDeck(unittest.TestCase):

    def test_get_user_deck_nominal_one_deck(self):
        db = SessionLocal()
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        name = "Yugi"
        password = "kingofgames"
        deckstring = "Mammoth Graveyard#Summoned Skill#Dark Magician Girl"
        db_record = User(name=name, password=password, wins=0, losses=0, draws=0, decks=deckstring)
        db.add(db_record)
        db.commit()
        deck = get_deck_from_db(name, 0)
        self.assertEqual(3, len(deck))
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        db.close()

    def test_get_user_deck_nominal_multiple_decks(self):
        db = SessionLocal()
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        name = "Yugi"
        password = "kingofgames"
        deckstring1 = "Mammoth Graveyard#Summoned Skill#Dark Magician Girl"
        deckstring2 = "Dark Magician#Gaia the Fierce Knight#Black Luster Soldier"
        deckstring = deckstring1 + "*" + deckstring2
        db_record = User(name=name, password=password, wins=0, losses=0, draws=0, decks=deckstring)
        db.add(db_record)
        db.commit()
        deck = get_deck_from_db(name, 1)
        self.assertEqual(3, len(deck))
        self.assertEqual("Dark Magician", deck[0])
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        db.close()

    def test_get_user_deck_invalid_index(self):
        db = SessionLocal()
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        name = "Yugi"
        password = "kingofgames"
        deckstring = "Mammoth Graveyard#Summoned Skill#Dark Magician Girl"
        db_record = User(name=name, password=password, wins=0, losses=0, draws=0, decks=deckstring)
        db.add(db_record)
        db.commit()
        deck = get_deck_from_db(name, 1)
        self.assertEqual(0, len(deck))
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        db.close()


class TestGetCardInfo(unittest.TestCase):
    def test_get_card_nominal_monster(self):
        db = SessionLocal()
        stmt = Cards.__table__.delete().where(Cards.name != "")
        engine.execute(stmt)
        read_cards_into_db()
        card_name = "Dark Magician"
        card_params = get_card_info(card_name)
        self.assertEqual("Dark Magician", card_params[0])
        self.assertEqual("", card_params[1])
        self.assertEqual("Dark", card_params[2])
        self.assertEqual("Spellcaster", card_params[3])
        self.assertEqual(7, card_params[4])
        self.assertEqual(2500, card_params[5])
        self.assertEqual(2100, card_params[6])
        stmt = Cards.__table__.delete().where(Cards.name != "")
        engine.execute(stmt)
        db.close()

    def test_get_card_spell_no_args(self):
        db = SessionLocal()
        stmt = Cards.__table__.delete().where(Cards.name != "")
        engine.execute(stmt)
        read_cards_into_db()
        card_name = "Dark Hole"
        card_params = get_card_info(card_name)
        self.assertEqual("Dark Hole", card_params[0])
        self.assertEqual("Normal", card_params[1])
        self.assertEqual('"Destroy all monsters on the field."', card_params[2])
        self.assertEqual("destroy_all_monsters", card_params[3])
        stmt = Cards.__table__.delete().where(Cards.name != "")
        engine.execute(stmt)
        db.close()

    def test_get_card_spell_with_args(self):
        db = SessionLocal()
        stmt = Cards.__table__.delete().where(Cards.name != "")
        engine.execute(stmt)
        read_cards_into_db()
        card_name = "Book of Secret Arts"
        card_params = get_card_info(card_name)
        self.assertEqual(card_name, card_params[0])
        self.assertEqual("Equip", card_params[1])
        description = '"A Spellcaster-Type monster equipped with this card increases its ATK and DEF by 300 points."'
        self.assertEqual(description, card_params[2])
        self.assertEqual("alter_monster_stats", card_params[3])
        self.assertEqual("300", card_params[4])
        self.assertEqual("300", card_params[5])
        self.assertEqual("Spellcaster", card_params[6])
        stmt = Cards.__table__.delete().where(Cards.name != "")
        engine.execute(stmt)
        db.close()

    def test_get_card_nonexistent(self):
        db = SessionLocal()
        stmt = Cards.__table__.delete().where(Cards.name != "")
        engine.execute(stmt)
        read_cards_into_db()
        card_name = "Black Luster Soldier, Envoy of the Beginning"
        card_params = get_card_info(card_name)
        self.assertEqual(0, len(card_params))
        stmt = Cards.__table__.delete().where(Cards.name != "")
        engine.execute(stmt)
        db.close()


class TestPrintUserDecks(unittest.TestCase):
    def test_print_user_decks_multiple(self):
        db = SessionLocal()
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        name = "Yugi"
        password = "kingofgames"
        deckstring1 = "Mammoth Graveyard#Summoned Skill#Dark Magician Girl"
        deckstring2 = "Dark Magician#Gaia the Fierce Knight#Black Luster Soldier"
        deckstring = deckstring1 + "*" + deckstring2
        db_record = User(name=name, password=password, wins=0, losses=0, draws=0, decks=deckstring)
        db.add(db_record)
        db.commit()
        print_user_decks(name)
        stmt = User.__table__.delete().where(User.name != "")
        engine.execute(stmt)
        db.close()
