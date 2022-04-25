import unittest
from src.card import Card, create_card, create_deck_from_preset, create_deck_from_array, \
    monster_card_dict_to_card_object
from src.card import Monster


class TestGameMethods(unittest.TestCase):
    def test_create_card_from_name_valid(self):
        card = create_card("Tomozaurus")
        self.assertEqual("Tomozaurus", card.name)
        card = create_card("Hitotsu-Me Giant")
        self.assertEqual("Hitotsu-Me Giant", card.name)

    def test_create_card_name_not_exists(self):
        card = create_card("vcwefw")
        self.assertEqual(None, card)

    def test_create_deck_from_csv(self):
        deck = create_deck_from_preset("sources/preset1")
        real_deck = [create_card("Hitotsu-Me Giant"), create_card("Dark Magician"), create_card("The Fierce Knight"),
                     create_card("Mammoth Graveyard"), create_card("Silver Fang"),
                     create_card("Curtian of the Dark One"), create_card("Tomozaurus"), create_card("Feral Imp")]
        self.assertEqual(len(real_deck), len(deck))
        for i in range(8):
            self.assertEqual(deck[0].name, real_deck[0].name)

    def test_create_deck_from_array(self):
        deck = create_deck_from_array(["Hitotsu-Me Giant", "Dark Magician", "The Fierce Knight", "Mammoth Graveyard",
                                       "Silver Fang", "Curtian of the Dark One", "Tomozaurus", "Feral Imp"])
        real_deck = [create_card("Hitotsu-Me Giant"), create_card("Dark Magician"), create_card("The Fierce Knight"),
                     create_card("Mammoth Graveyard"), create_card("Silver Fang"),
                     create_card("Curtian of the Dark One"), create_card("Tomozaurus"), create_card("Feral Imp")]
        self.assertEqual(len(real_deck), len(deck))
        for i in range(8):
            self.assertEqual(deck[0].name, real_deck[0].name)


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

    def test_monster_dict_to_object(self):
        obj = monster_card_dict_to_card_object(
            {"name": "Hitotsu-Me Giant", "card_type": "Monster", "attribute": "Earth",
             "monster_type": "Beast-Warrior",
             "level": 4, "attack_points": 1200, "defense_points": 1000, "id": 76184692, "description": "test"})
        self.assertEqual(obj.name, "Hitotsu-Me Giant")
        self.assertEqual(obj.card_type, "Monster")
        self.assertEqual(obj.attribute, "Earth")
        self.assertEqual(obj.monster_type, "Beast-Warrior")
        self.assertEqual(obj.attack_points, 1200)
        self.assertEqual(obj.defense_points, 1000)
        self.assertEqual(obj.description, "test")

