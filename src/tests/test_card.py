import unittest
from src.card import Card
from src.card import Monster


class TestCard(unittest.TestCase):
    def test_display_card_card_correct_inputs(self):
        test_card_1 = Card("Hitotsu-Me Giant", "A behemoth", "Monster")
        test_card_2 = Card("Dark Magician", "None", "Monster")
        test_card_3 = Card("Gaia The Fierce Knight", "None", "Monster")

        result_1 = test_card_1.display_card()
        self.assertEqual(result_1["name"], "Hitotsu-Me Giant")
        self.assertEqual(result_1["card_type"], "Monster")
        self.assertEqual(result_1["description"], "A behemoth")

        result_2 = test_card_2.display_card()
        self.assertEqual(result_2["name"], "Dark Magician")
        self.assertEqual(result_2["card_type"], "Monster")
        self.assertEqual(result_2["description"], "None")

        result_3 = test_card_3.display_card()
        self.assertEqual(result_3["name"], "Gaia The Fierce Knight")
        self.assertEqual(result_3["card_type"], "Monster")
        self.assertEqual(result_3["description"], "None")


class TestMonster(unittest.TestCase):
    def test_display_card_monster_correct_inputs(self):
        test_card_1 = Monster("Hitotsu-Me Giant", "A behemoth", "Earth", "Beast-Warrior", 4, 1200, 1000)
        test_card_2 = Monster("Dark Magician", "None", "Dark", "Spellcaster", 7, 2500, 2100)
        test_card_3 = Monster("Gaia The Fierce Knight", "None", "Earth", "Warrior", 7, 2300, 2100)
        result_1 = test_card_1.display_card()
        result_2 = test_card_2.display_card()
        result_3 = test_card_3.display_card()
        self.assertEqual(result_1["name"], "Hitotsu-Me Giant")
        self.assertEqual(result_1["card_type"], "Monster")
        self.assertEqual(result_1["description"], "A behemoth")
        self.assertEqual(result_1["attribute"], "Earth")
        self.assertEqual(result_1["level"], 4)
        self.assertEqual(result_1["ATK"], 1200)
        self.assertEqual(result_1["DEF"], 1000)

        self.assertEqual(result_2["name"], "Dark Magician")
        self.assertEqual(result_2["card_type"], "Monster")
        self.assertEqual(result_2["description"], "None")
        self.assertEqual(result_2["attribute"], "Dark")
        self.assertEqual(result_2["level"], 7)
        self.assertEqual(result_2["ATK"], 2500)
        self.assertEqual(result_2["DEF"], 2100)

        self.assertEqual(result_3["name"], "Gaia The Fierce Knight")
        self.assertEqual(result_3["card_type"], "Monster")
        self.assertEqual(result_3["description"], "None")
        self.assertEqual(result_3["attribute"], "Earth")
        self.assertEqual(result_3["level"], 7)
        self.assertEqual(result_3["ATK"], 2300)
        self.assertEqual(result_3["DEF"], 2100)
