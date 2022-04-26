import unittest
from src.database import SessionLocal
from src.database import Cards
from src.database import User
from src.database import engine
from src.database_functions import read_cards_into_db
from src.database_functions import login
from src.database_functions import register
from sqlalchemy import select


class TestReadCards(unittest.TestCase):
    def test_read_cards_nominal(self):
        read_cards_into_db()
        db = SessionLocal()
        db_record = db.scalars(select(Cards)).first()
        self.assertEqual("Hitotsu-Me Giant", db_record.name)
        Cards.__table__.drop(engine)
        db.close()


# class TestRegister(unittest.TestCase):
#     def test_register_nominal(self):
#         db = SessionLocal()
#         name = "Yugi"
#         password = "kingofgames"
#         success = register(name, password)
#         User.__table__.drop(engine)
#         self.assertEqual(True, success)
#         db.close()

class TestLogin(unittest.TestCase):
    def test_login_nominal(self):
        db = SessionLocal()
        name = "Yugi"
        password = "kingofgames"
        register(name, password)
        success = login(name, password)
        User.__table__.drop(engine)
        self.assertEqual(True, success)
        db.close()
