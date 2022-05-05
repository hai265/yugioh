import unittest
from unittest.mock import patch
from src.account_menu import display_prompt, login_proxy, register_proxy
from src.database import SessionLocal
from src.database import User
from src.database import engine


class TestDisplayPrompt(unittest.TestCase):

    @patch('builtins.input', side_effect=['2', 'Yugi', 'kingofgames'])
    def test_display_register(self, mock_input):
        db = SessionLocal()
        result = display_prompt()
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        db.close()
        self.assertEqual(result["name"], "Yugi")  # add assertion here
        self.assertEqual(result["wins"], 0)
        self.assertEqual(result["losses"], 0)
        self.assertEqual(result["draws"], 0)

    @patch('builtins.input', side_effect=['1', 'Yugi', 'kingofgames'])
    def test_display_login(self, mock_input):
        db = SessionLocal()
        db_record = User(name="Yugi", password="kingofgames", wins=34, losses=5, draws=1)
        db.add(db_record)
        db.commit()
        result = display_prompt()
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        db.close()
        self.assertEqual(result["name"], "Yugi")  # add assertion here
        self.assertEqual(result["wins"], 34)
        self.assertEqual(result["losses"], 5)
        self.assertEqual(result["draws"], 1)

    @patch('builtins.input', side_effect=['0', '0', '3', '2', 'Yugi', 'kingofgames'])
    def test_display_invalid_function_to_valid(self, mock_input):
        db = SessionLocal()
        result = display_prompt()
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        db.close()
        self.assertEqual(result["name"], "Yugi")  # add assertion here
        self.assertEqual(result["wins"], 0)
        self.assertEqual(result["losses"], 0)
        self.assertEqual(result["draws"], 0)


class TestRegisterProxy(unittest.TestCase):

    @patch('builtins.input', side_effect=['Yugi', 'kingofgames'])
    def test_register_proxy_nominal(self, mock_input):
        db = SessionLocal()
        result = register_proxy()
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        db.close()
        self.assertEqual(result["name"], "Yugi")  # add assertion here
        self.assertEqual(result["wins"], 0)
        self.assertEqual(result["losses"], 0)
        self.assertEqual(result["draws"], 0)

    @patch('builtins.input', side_effect=['', 'Yugi', 'kingofgames'])
    def test_register_proxy_empty_name_to_nominal(self, mock_input):
        db = SessionLocal()
        result = register_proxy()
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        db.close()
        self.assertEqual(result["name"], "Yugi")  # add assertion here
        self.assertEqual(result["wins"], 0)
        self.assertEqual(result["losses"], 0)
        self.assertEqual(result["draws"], 0)

    @patch('builtins.input', side_effect=['Yugi', '', 'kingofgames'])
    def test_register_proxy_empty_password_to_nominal(self, mock_input):
        db = SessionLocal()
        result = register_proxy()
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        db.close()
        self.assertEqual(result["name"], "Yugi")  # add assertion here
        self.assertEqual(result["wins"], 0)
        self.assertEqual(result["losses"], 0)
        self.assertEqual(result["draws"], 0)

    @patch('builtins.input', side_effect=['Yugi', 'kingofgames', 'Yugi', 'Kaiba', 'blueeyes'])
    def test_register_proxy_duplicate_user_to_nominal(self, mock_input):
        db = SessionLocal()
        register_proxy()
        result = register_proxy()
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        stmt = User.__table__.delete().where(User.name == "Kaiba")
        engine.execute(stmt)
        db.close()
        self.assertEqual(result["name"], "Kaiba")  # add assertion here
        self.assertEqual(result["wins"], 0)
        self.assertEqual(result["losses"], 0)
        self.assertEqual(result["draws"], 0)


class TestLoginProxy(unittest.TestCase):
    @patch('builtins.input', side_effect=['Yugi', 'kingofgames'])
    def test_login_proxy_nominal(self, mock_input):
        db = SessionLocal()
        db_record = User(name="Yugi", password="kingofgames", wins=34, losses=5, draws=1)
        db.add(db_record)
        db.commit()
        result = login_proxy()
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        db.close()
        self.assertEqual(result["name"], "Yugi")  # add assertion here
        self.assertEqual(result["wins"], 34)
        self.assertEqual(result["losses"], 5)
        self.assertEqual(result["draws"], 1)

    @patch('builtins.input', side_effect=['nonexistent', 'Yugi', 'kingofgames'])
    def test_login_proxy_nonexistent_user_to_nominal(self, mock_input):
        db = SessionLocal()
        db_record = User(name="Yugi", password="kingofgames", wins=34, losses=5, draws=1)
        db.add(db_record)
        db.commit()
        result = login_proxy()
        stmt = User.__table__.delete().where(User.name == "Yugi")
        engine.execute(stmt)
        db.close()
        self.assertEqual(result["name"], "Yugi")  # add assertion here
        self.assertEqual(result["wins"], 34)
        self.assertEqual(result["losses"], 5)
        self.assertEqual(result["draws"], 1)