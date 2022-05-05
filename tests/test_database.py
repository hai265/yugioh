import unittest
from src.database import SessionLocal
from src.database import Cards
from src.database import User
from src.database import engine
from src.database_functions import read_cards_into_db
from src.database_functions import login, register, get_user_stats, user_exists
from sqlalchemy import select


class TestReadCards(unittest.TestCase):
    def test_read_cards_nominal(self):
        read_cards_into_db()
        db = SessionLocal()
        db_record = db.scalars(select(Cards)).first()
        self.assertEqual("Monster", db_record.card_type)
        Cards.__table__.drop(engine)
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
        db_record = User(name=name, password=password, wins=34, losses=5, draws=1)
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
