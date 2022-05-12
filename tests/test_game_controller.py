import unittest
from src.card import create_card, create_deck_from_array, Monster, Spell
from src.card_effects import *
from src.player import Player
from src.game import GameController


class TestGameController(unittest.TestCase):
    def setUp(self) -> None:
        # ATK for Curtain of the Dark One is 600 and ATK for Hitotsu-Me Giant 1200
        self.player1_card1 = create_card('Curtain of the Dark One')
        self.player1_card2 = create_card('Hitotsu-Me Giant')

        self.player2_card1 = create_card('Curtain of the Dark One')
        self.player2_card2 = create_card('Hitotsu-Me Giant')

        self.player1 = Player(5000, 'Yugi')
        self.player2 = Player(5000, 'Kaiba')

        self.player1.hand = [self.player1_card1, self.player1_card2]
        self.player2.hand = [self.player2_card1, self.player2_card2]

        self.game = GameController(None)
        self.game.players = [self.player1, self.player2]

    def test_change_turns(self):
        self.game.change_turn()
        current = self.game.get_current_player()
        other = self.game.get_other_player()
        self.assertEqual(self.player2, current)
        self.assertEqual(self.player1, other)

        self.game.change_turn()
        current = self.game.get_current_player()
        other = self.game.get_other_player()
        self.assertEqual(self.player1, current)
        self.assertEqual(self.player2, other)

    def test_summon_monsters(self):
        # player1 summon
        current = self.game.get_current_player()

        self.game.normal_summon(0)
        self.assertEqual(1, current.get_hand_size())
        self.assertEqual(self.player1_card1, current.monster_field[0])
        # change turn
        self.game.change_turn()

        current = self.game.get_current_player()
        # player2 summon
        self.game.normal_summon(1)
        self.assertEqual(1, current.get_hand_size())
        self.assertEqual(self.player2_card2, current.monster_field[0])

    def test_attack_monster_attacker_loses(self):
        # summon monsters
        self.game.normal_summon(0)
        self.game.change_turn()
        self.game.normal_summon(1)
        self.game.change_turn()

        # player0 monster attacks player1 monster
        # lp lost will be abs(600 - 1200) = 600 and attacking monster will be destroyed
        # lp will be lost from attacking player
        self.game.attack_monster(0, 0)

        current = self.game.get_current_player()
        other = self.game.get_other_player()

        self.assertEqual(None, current.monster_field[0])
        self.assertNotEqual(None, other.monster_field[0])

        self.assertEqual(1, current.get_graveyard_size())
        self.assertEqual(0, other.get_graveyard_size())

        self.assertEqual(4400, current.life_points)
        self.assertEqual(5000, other.life_points)

    def test_attack_monster_attacker_ties(self):
        # summon monsters
        self.game.normal_summon(0)
        self.game.change_turn()
        self.game.normal_summon(0)
        self.game.change_turn()

        # player0 monster attacks player1 monster
        # lp lost will be abs(600 - 600) = 0 and both monsters will be destroyed
        self.game.attack_monster(0, 0)

        current = self.game.get_current_player()
        other = self.game.get_other_player()

        self.assertEqual(None, current.monster_field[0])
        self.assertEqual(None, other.monster_field[0])

        self.assertEqual(1, current.get_graveyard_size())
        self.assertEqual(1, other.get_graveyard_size())

        self.assertEqual(5000, current.life_points)
        self.assertEqual(5000, other.life_points)

    def test_attack_monster_attacker_wins(self):
        # summon monsters
        self.game.normal_summon(1)
        self.game.change_turn()
        self.game.normal_summon(0)
        self.game.change_turn()

        # player0 monster attacks player1 monster
        # lp lost will be abs(1200 - 600) = 600 and the targeted monster will be destroyed
        # lp will be lost from attacked player
        self.game.attack_monster(0, 0)

        current = self.game.get_current_player()
        other = self.game.get_other_player()

        self.assertNotEqual(None, current.monster_field[0])
        self.assertEqual(None, other.monster_field[0])

        self.assertEqual(0, current.get_graveyard_size())
        self.assertEqual(1, other.get_graveyard_size())

        self.assertEqual(5000, current.life_points)
        self.assertEqual(4400, other.life_points)

    def test_attack_directly(self):
        # summon monsters
        self.game.normal_summon(1)
        self.game.change_turn()
        # skip second player's turn
        self.game.change_turn()

        self.game.attack_player(0)

        current = self.game.get_current_player()
        other = self.game.get_other_player()

        # lp lost will be 1200, attacked player should now have 5000 - 1200 = 3800 lp left
        self.assertEqual(5000, current.life_points)
        self.assertEqual(3800, other.life_points)

    def test_attack_from_defense_position(self):
        self.game.normal_set(1)
        self.game.change_turn()
        self.game.normal_summon(0)
        self.game.change_turn()

        self.game.attack_monster(0, 0)

        current = self.game.get_current_player()
        other = self.game.get_other_player()

        # nothing should happen
        self.assertEqual(5000, current.life_points)
        self.assertEqual(5000, other.life_points)
        self.assertEqual(self.player1_card2, self.player1.monster_field[0])
        self.assertEqual(self.player2_card1, self.player2.monster_field[0])

    def test_attack_monster_in_defense_position_attacker_wins(self):
        self.game.normal_summon(1)
        self.game.change_turn()
        self.game.normal_set(0)
        self.game.change_turn()

        self.game.attack_monster(0, 0)

        current = self.game.get_current_player()
        other = self.game.get_other_player()

        # nothing should happen to life points
        self.assertEqual(5000, current.life_points)
        self.assertEqual(5000, other.life_points)

        # check monster field
        self.assertEqual(self.player1_card2, self.player1.monster_field[0])
        self.assertEqual(None, self.player2.monster_field[0])

        # check graveyard
        self.assertEqual([], self.player1.graveyard)
        self.assertEqual([self.player2_card1], self.player2.graveyard)

    def test_attack_monster_in_defense_position_attacker_loses(self):
        self.game.normal_summon(0)
        self.game.change_turn()
        self.game.normal_set(1)
        self.game.change_turn()

        self.game.attack_monster(0, 0)

        current = self.game.get_current_player()
        other = self.game.get_other_player()

        # nothing should happen to life points
        self.assertEqual(4600, current.life_points)
        self.assertEqual(5000, other.life_points)

        # check monster field
        self.assertEqual(self.player1_card1, self.player1.monster_field[0])
        self.assertEqual(self.player2_card2, self.player2.monster_field[0])
        self.assertEqual(Monster.FACE_UP, self.player2.monster_field[0].face_pos)
        self.assertEqual(Monster.DEF, self.player2.monster_field[0].battle_pos)

        # check graveyard
        self.assertEqual([], self.player1.graveyard)
        self.assertEqual([], self.player2.graveyard)

    def test_flip_summon_then_attack(self):
        self.game.normal_set(1)
        self.game.change_turn()
        self.game.normal_summon(0)
        self.game.change_turn()

        self.game.flip_summon(0)

        self.assertEqual(Monster.FACE_UP, self.player1.monster_field[0].face_pos)
        self.assertEqual(Monster.ATK, self.player1.monster_field[0].battle_pos)

        self.game.attack_monster(0, 0)

        self.assertTrue(self.player2.monster_field[0] is None)
        self.assertEqual([self.player2_card1], self.player2.graveyard)

    def test_attack_directly_fails(self):
        # summon monsters
        self.game.normal_summon(1)
        self.game.change_turn()
        self.game.normal_summon(1)
        self.game.change_turn()

        self.game.attack_player(0)

        current = self.game.get_current_player()
        other = self.game.get_other_player()

        # Nothing should happen since attacked player has monsters on their field
        self.assertEqual(5000, current.life_points)
        self.assertEqual(5000, other.life_points)

    def test_attack_directly_ends_game(self):
        # set life points for players
        self.player1.life_points = 1000
        self.player2.life_points = 1000

        # summon monsters
        self.game.normal_summon(1)
        self.game.change_turn()
        # skip second player's turn
        self.game.change_turn()

        self.game.attack_player(0)

        current = self.game.get_current_player()
        other = self.game.get_other_player()

        # attacked player will lose 1200 lp but since they only have 1000 lp their new total should be 0
        self.assertEqual(1000, current.life_points)
        self.assertEqual(0, other.life_points)
    
    def test_is_there_winner(self):
        self.player2.life_points = 0
        self.assertTrue(self.game.is_there_winner())

    def test_get_winner(self):
        self.player2.life_points = 0
        self.assertEqual(self.player1, self.game.get_winner())


class TestCanAttack(unittest.TestCase):
    def setUp(self) -> None:
        # ATK for Curtain of the Dark One is 600 and ATK for Hitotsu-Me Giant 1200
        self.player1_card1 = create_card('Curtain of the Dark One')
        self.player1_card2 = create_card('Hitotsu-Me Giant')
        self.player1_card3 = create_card('Dark Magician')

        self.player2_card1 = create_card('Curtain of the Dark One')
        self.player2_card2 = create_card('Hitotsu-Me Giant')
        self.player2_card3 = create_card('Dark Magician')
        self.player1 = Player(5000, 'Yugi')
        self.player2 = Player(5000, 'Kaiba')

        self.player1.hand = [self.player1_card1, self.player1_card2, self.player1_card3]
        self.player2.hand = [self.player2_card1, self.player2_card2, self.player1_card3]

        self.game = GameController(None)
        self.game.players = [self.player1, self.player2]
    
    def test_can_attack_normal_summon(self):
        # player1 summon
        current = self.game.get_current_player()
        self.game.normal_summon(0)
        self.assertFalse(current.monster_field[0].can_attack)
        # change turn
        self.game.change_turn()
        current = self.game.get_current_player()
        # player2 summon
        self.game.normal_summon(1)
        self.assertTrue(current.monster_field[0].can_attack)

    def test_can_attack_change_turn(self):
        current = self.game.get_current_player()
        self.game.normal_summon(0)
        self.game.change_turn()
        self.assertTrue(current.monster_field[0].can_attack)
        current = self.game.get_current_player()
        self.game.normal_summon(0)
        self.game.change_turn()
        self.assertTrue(current.monster_field[0].can_attack)

    def test_can_attack_tribute_summon(self):
        # player1 summon
        current = self.game.get_current_player()
        self.game.normal_summon(0)
        self.game.normal_summon(0)
        self.game.tribute_summon_monster(0, 0, 1)
        self.assertFalse(current.monster_field[0].can_attack)
        # change turn
        self.game.change_turn()
        current = self.game.get_current_player()
        self.game.normal_summon(0)
        self.game.normal_summon(0)
        self.game.tribute_summon_monster(0, 0, 1)
        self.assertTrue(current.monster_field[0].can_attack)

    def test_can_attack_attack_player(self):
        self.game.change_turn()
        current = self.game.get_current_player()
        self.game.normal_summon(0)
        self.game.attack_player(0)
        self.assertFalse(current.monster_field[0].can_attack)
    
    def test_can_attack_attack_monster(self):
        self.game.normal_summon(0)
        self.game.change_turn()
        self.game.normal_summon(1)
        self.game.attack_monster(0, 0)
        self.assertFalse(self.game.get_current_player().monster_field[0].can_attack)

    def test_can_attack_normal_set(self):
        self.game.normal_set(0)
        self.assertFalse(self.game.get_current_player().monster_field[0].can_attack)
        self.game.change_turn()
        self.assertFalse(self.game.get_other_player().monster_field[0].can_attack)
        self.game.normal_set(0)
        self.assertFalse(self.game.get_current_player().monster_field[0].can_attack)


        self.game.attack_monster(0, 0)
class TestNormalSpellCards(unittest.TestCase):
    def setUp(self):
        self.player1 = Player(5000, 'Yugi')
        self.player2 = Player(5000, 'Kaiba')

        p1_effects = Effect(self.player1, self.player2)
        p2_effects = Effect(self.player2, self.player1)
        spell_names = ["Dark Hole", "Dian Keto the Cure Master", "Fissure", "Ookazi"]

        self.p1_spells = create_deck_from_array(spell_names, p1_effects)
        self.p2_spells = create_deck_from_array(spell_names, p2_effects)

        self.player1_card1 = create_card('Curtain of the Dark One')
        self.player1_card2 = create_card('Hitotsu-Me Giant')

        self.player2_card1 = create_card('Curtain of the Dark One')
        self.player2_card2 = create_card('Hitotsu-Me Giant')

        self.game = GameController(None)

        self.game.players = [self.player1, self.player2]

    def test_dark_hole_spell_card(self):
        # add spell to hand
        self.game.get_current_player().hand.insert(0, self.p1_spells[0])
        self.game.get_other_player().hand.insert(0, self.p2_spells[0])

        # set up field
        self.game.get_current_player().monster_field = [self.player1_card1, self.player1_card2, None, None, None]
        self.game.get_other_player().monster_field = [self.player2_card1, self.player2_card2, None, None, None]

        # use spell card
        expected_field = [None] * Player.FIELD_CARD_LIMIT
        expected_graveyard_p1 = [create_card('Curtain of the Dark One'), create_card('Hitotsu-Me Giant'),
                                 self.p1_spells[0]]
        expected_graveyard_p2 = [create_card('Curtain of the Dark One'), create_card('Hitotsu-Me Giant')]

        self.game.activate_spell(0)

        self.assertEqual(expected_field, self.game.get_current_player().monster_field)
        self.assertEqual(expected_graveyard_p1, self.game.get_current_player().graveyard)

        self.assertEqual(expected_field, self.game.get_other_player().monster_field)
        self.assertEqual(expected_graveyard_p2, self.game.get_other_player().graveyard)

    def test_dian_keto_spell_card(self):
        # add spell to hand
        self.game.get_current_player().hand.insert(0, self.p1_spells[1])

        # use spell card
        self.game.activate_spell(0)
        self.assertEqual(6000, self.game.get_current_player().life_points)

        # check graveyard
        self.assertEqual([self.p1_spells[1]], self.game.get_current_player().graveyard)

    def test_fissure_spell_card(self):
        # add spell to hand
        self.game.get_current_player().hand.insert(0, self.p1_spells[2])
        self.game.get_other_player().hand.insert(0, self.p2_spells[2])

        # set up field
        self.game.get_current_player().monster_field = [self.player1_card1, self.player1_card2, None, None, None]
        self.game.get_other_player().monster_field = [self.player2_card1, self.player2_card2, None, None, None]

        # use spell card
        expected_field = [None, create_card('Hitotsu-Me Giant'), None, None, None]
        expected_graveyard = [create_card('Curtain of the Dark One')]

        self.game.activate_spell(0)

        self.assertEqual(expected_field, self.game.get_other_player().monster_field)
        self.assertEqual(expected_graveyard, self.game.get_other_player().graveyard)

        # check current player graveyard
        self.assertEqual([self.p2_spells[2]], self.game.get_current_player().graveyard)

    def test_fissure_spell_card_equal_attack_case(self):
        # add spell to hand
        self.game.get_current_player().hand.insert(0, self.p1_spells[2])
        self.game.get_other_player().hand.insert(0, self.p2_spells[2])

        # set up field
        self.game.get_current_player().monster_field = [self.player1_card1, self.player1_card2, None, None, None]
        self.game.get_other_player().monster_field = [self.player2_card1, create_card('Curtain of the Dark One'),
                                                      None, None, None]

        # use spell card
        expected_field = [None, create_card('Curtain of the Dark One'), None, None, None]
        expected_graveyard = [create_card('Curtain of the Dark One')]

        self.game.activate_spell(0)

        self.assertEqual(expected_field, self.game.get_other_player().monster_field)
        self.assertEqual(expected_graveyard, self.game.get_other_player().graveyard)

        # check current player graveyard
        self.assertEqual([self.p2_spells[2]], self.game.get_current_player().graveyard)

    def test_ookazi_spell_card(self):
        # add spell to hand
        self.game.get_current_player().hand.insert(0, self.p1_spells[3])

        # use spell card
        self.game.activate_spell(0)
        self.assertEqual(4200, self.game.get_other_player().life_points)

        # check current player graveyard
        self.assertEqual([self.p1_spells[3]], self.game.get_current_player().graveyard)

    def test_spell_cards_in_different_turns(self):
        # add dark hold and dian keto to p1 hand
        self.game.get_current_player().hand = self.p1_spells[:2] + [self.player1_card1, self.player1_card2]

        # add fissure and ookazi to p2 hand
        self.game.get_other_player().hand = [self.p2_spells[2], self.p2_spells[3]] + [self.player2_card1,
                                                                                      self.player2_card2]

        # summon monsters
        self.game.normal_summon(2)
        self.game.change_turn()
        self.game.normal_summon(2)

        # p2 uses fissure spell
        expected_p1_field = [None] * Player.FIELD_CARD_LIMIT
        expected_p1_graveyard = [create_card('Curtain of the Dark One')]

        self.game.activate_spell(0)

        self.assertEqual(expected_p1_field, self.game.get_other_player().monster_field)
        self.assertEqual(expected_p1_graveyard, self.game.get_other_player().graveyard)
        self.assertEqual([self.p2_spells[2]], self.game.get_current_player().graveyard)

        # p2 attacks p1
        self.game.attack_player(0)
        self.assertEqual(4400, self.game.get_other_player().life_points)

        self.game.change_turn()

        # p1 uses dian keto spell
        self.game.activate_spell(1)
        self.assertEqual(5400, self.game.get_current_player().life_points)

        # check p1 graveyard
        expected_p1_graveyard.append(self.p2_spells[1])
        self.assertEqual(expected_p1_graveyard, self.game.get_current_player().graveyard)


class TestEquipSpellCards(unittest.TestCase):
    def setUp(self):
        self.player1 = Player(5000, 'Yugi')
        self.player2 = Player(5000, 'Kaiba')

        p1_effects = Effect(self.player1, self.player2)
        p2_effects = Effect(self.player2, self.player1)
        spell_names = ["Book of Secret Arts", "Sword of Dark Destruction", "Dark Energy", "Invigoration"]

        self.p1_spells = create_deck_from_array(spell_names, p1_effects)
        self.p2_spells = create_deck_from_array(spell_names, p2_effects)

        self.player1_card1 = create_card('Curtain of the Dark One')
        self.player1_card2 = create_card('Hitotsu-Me Giant')

        self.player2_card1 = create_card('Curtain of the Dark One')
        self.player2_card2 = create_card('Hitotsu-Me Giant')

        self.game = GameController(None)

        self.game.players = [self.player1, self.player2]

    def test_book_of_secret_arts_spell(self):
        # set hand and field
        current = self.game.get_current_player()
        current.hand = [self.p1_spells[0]]
        current.monster_field[0] = create_card('Curtain of the Dark One')

        # use equip spell card
        self.game.equip_spell(0, 0)

        self.assertEqual(900, current.monster_field[0].attack_points)
        self.assertEqual(800, current.monster_field[0].defense_points)

    def test_sword_of_dark_destruction_spell(self):
        # set hand and field
        current = self.game.get_current_player()
        current.hand = [self.p1_spells[1]]
        current.monster_field[0] = create_card('Curtain of the Dark One')

        # use equip spell card
        self.game.equip_spell(0, 0)

        self.assertEqual(1000, current.monster_field[0].attack_points)
        self.assertEqual(300, current.monster_field[0].defense_points)

    def test_dark_energy_spell(self):
        # set hand and field
        current = self.game.get_current_player()
        current.hand = [self.p1_spells[2]]
        current.monster_field[0] = create_card('Feral Imp')

        # use equip spell card
        self.game.equip_spell(0, 0)

        self.assertEqual(1600, current.monster_field[0].attack_points)
        self.assertEqual(1700, current.monster_field[0].defense_points)

    def test_invigoration_spell(self):
        # set hand and field
        current = self.game.get_current_player()
        current.hand = [self.p1_spells[3]]
        current.monster_field[0] = create_card('Tomozaurus')

        # use equip spell card
        self.game.equip_spell(0, 0)

        self.assertEqual(900, current.monster_field[0].attack_points)
        self.assertEqual(200, current.monster_field[0].defense_points)

    def test_remove_book_of_secret_arts_spell(self):
        # set hand and field
        current = self.game.get_current_player()
        current.hand = [self.p1_spells[0]]
        current.monster_field[0] = create_card('Curtain of the Dark One')

        # use equip spell card
        self.game.equip_spell(0, 0)

        self.assertEqual(900, current.monster_field[0].attack_points)
        self.assertEqual(800, current.monster_field[0].defense_points)

        # remove equip card
        self.game.get_current_player().send_card_to_graveyard(-1, -1, 0)

        # check monster stats
        self.assertEqual(600, current.monster_field[0].attack_points)
        self.assertEqual(500, current.monster_field[0].defense_points)

        # check graveyard
        self.assertEqual([self.p1_spells[0]], self.game.get_current_player().graveyard)

    def test_remove_equipped_monster(self):
        # set hand and field
        current = self.game.get_current_player()
        current.hand = [self.p1_spells[0]]
        current.monster_field[0] = create_card('Curtain of the Dark One')

        # use equip spell card
        self.game.equip_spell(0, 0)

        self.assertEqual(900, current.monster_field[0].attack_points)
        self.assertEqual(800, current.monster_field[0].defense_points)

        # remove monster
        self.game.get_current_player().send_card_to_graveyard(0, -1, -1)

        # check monster stats
        self.assertEqual(600, current.graveyard[0].attack_points)
        self.assertEqual(500, current.graveyard[0].defense_points)

        # check graveyard
        self.assertEqual([create_card('Curtain of the Dark One'), self.p1_spells[0]],
                         self.game.get_current_player().graveyard)
