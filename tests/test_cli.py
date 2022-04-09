import unittest
from src.CLIInterface import create_deck_from_preset
from src.CLIInterface import create_card


class TestCli(unittest.TestCase):
    def test_create_card_valid(self):
        card = create_card("Tomozaurus")
        self.assertEqual("Tomozaurus", card.name)

    def test_create_card_name_not_exists(self):
        card = create_card("vcwefw")
        self.assertEqual(None, card)

    def test_create_deck_from_preset(self):
        pass
        # deck = create_deck_from_preset("sources/preset1")
        # real_deck =
        # self.assertEqual()
