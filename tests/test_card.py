import unittest
from src.card import create_card, create_deck_from_preset, create_deck_from_array,\
    Monster


class TestGameMethods(unittest.TestCase):
    def test_create_card_from_name_valid(self):
        card = create_card("Tomozaurus")
        self.assertEqual("Tomozaurus", card.name)
        card = create_card("Hitotsu-Me Giant")
        self.assertEqual("Hitotsu-Me Giant", card.name)

    def test_create_card_name_not_exists(self):
        card = create_card("vcwefw")
        self.assertEqual(None, card)

    def test_create_deck_from_csvt(self):
        deck = create_deck_from_preset("sources/preset1")
        real_deck = [create_card("Hitotsu-Me Giant"), create_card("Dark Magician"), create_card("The Fierce Knight"),
                     create_card("Mammoth Graveyard"), create_card("Silver Fang"),
                     create_card("Curtain of the Dark One"), create_card("Tomozaurus"), create_card("Feral Imp")]
        self.assertEqual(len(real_deck), len(deck))
        for i in range(8):
            self.assertEqual(deck[0].name, real_deck[0].name)

    def test_create_deck_from_array(self):
        deck = create_deck_from_array(["Hitotsu-Me Giant", "Dark Magician", "The Fierce Knight", "Mammoth Graveyard",
                                       "Silver Fang", "Curtain of the Dark One", "Tomozaurus", "Feral Imp"])
        real_deck = [create_card("Hitotsu-Me Giant"), create_card("Dark Magician"), create_card("The Fierce Knight"),
                     create_card("Mammoth Graveyard"), create_card("Silver Fang"),
                     create_card("Curtain of the Dark One"), create_card("Tomozaurus"), create_card("Feral Imp")]
        self.assertEqual(len(real_deck), len(deck))
        for i in range(8):
            self.assertEqual(deck[0].name, real_deck[0].name)

    def test_create_spell_card(self):
        card1_repr = "name:Dark Hole, icon:normal, speed:1, position:up"
        card2_repr = "name:Dian Keto the Cure Master, icon:normal, speed:1, position:up"

        card1 = create_card("Dark Hole")
        self.assertEqual(card1_repr, repr(card1))

        card2 = create_card("Dian Keto the Cure Master")
        self.assertEqual(card2_repr, repr(card2))

    def test_create_spell_deck(self):
        card_names = ['Dark Hole', 'Dian Keto the Cure Master', 'Fissure', 'Ancient Telescope', 'Ookazi']
        expected_deck = [create_card(name) for name in card_names]

        self.assertEqual(expected_deck, create_deck_from_array(card_names))


class TestMonster(unittest.TestCase):
    def test_display_card_monster_correct_inputs(self):
        test_card_1 = Monster("Hitotsu-Me Giant", "A behemoth", "Earth", "Beast-Warrior", 4, 1200, 1000)
        test_card_2 = Monster("Dark Magician", "None", "Dark", "Spellcaster", 7, 2500, 2100)
        test_card_3 = Monster("Gaia The Fierce Knight", "None", "Earth", "Warrior", 7, 2300, 2100)

        card1_repr = "name:Hitotsu-Me Giant, level:4, attribute:Earth, type:Beast-Warrior, atk:1200, def:1000, " \
                     "face position:up, battle position:atk"
        card2_repr = "name:Dark Magician, level:7, attribute:Dark, type:Spellcaster, atk:2500, def:2100, " \
                     "face position:up, battle position:atk"
        card3_repr = "name:Gaia The Fierce Knight, level:7, attribute:Earth, type:Warrior, atk:2300, def:2100, " \
                     "face position:up, battle position:atk"

        result1 = repr(test_card_1)
        result2 = repr(test_card_2)
        result3 = repr(test_card_3)

        self.assertEqual(card1_repr, result1)
        self.assertEqual(card2_repr, result2)
        self.assertEqual(card3_repr, result3)
