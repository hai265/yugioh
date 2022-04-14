import unittest
from src.cli import create_card
from src.cli import create_deck_from_preset


class TestCli(unittest.TestCase):
    def test_create_card_from_name_valid(self):
        card = create_card("Tomozaurus")
        self.assertEqual("Tomozaurus", card.name)
        card = create_card("Hitotsu-Me Giant")
        self.assertEqual("Hitotsu-Me Giant", card.name)

    def test_create_card_name_not_exists(self):
        card = create_card("vcwefw")
        self.assertEqual(None, card)

    def test_create_deck_from_preset(self):
        deck = create_deck_from_preset("sources/preset1")
        real_deck = [create_card("Hitotsu-Me Giant"), create_card("Dark Magician"), create_card("The Fierce Knight"),
                     create_card("Mammoth Graveyard"), create_card("Silver Fang"), create_card("monster"),
                     create_card("Curtian of the Dark One"), create_card("Tomozaurus")]
        self.assertEqual(len(real_deck), len(deck))
        for i in range(8):
            self.assertEqual(deck[0].name, real_deck[0].name)
