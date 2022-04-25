import unittest
from src.card import create_card

from src.player import Player
# from src.card import Card
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

        self.game = GameController(self.player1, self.player2)

    def test_change_turns(self):
        self.game.change_turn()
        self.assertEqual(self.player2, self.game.current_player)
        self.assertEqual(self.player1, self.game.other_player)

        self.game.change_turn()
        self.assertEqual(self.player1, self.game.current_player)
        self.assertEqual(self.player2, self.game.other_player)

    def test_summon_monsters(self):
        # player1 summon
        self.game.normal_summon(0, 'atk')
        self.assertEqual(1, self.game.current_player.get_hand_size())
        self.assertEqual(self.player1_card1, self.game.current_player.monster_field[0])

        # change turn
        self.game.change_turn()

        # player2 summon
        self.game.normal_summon(1, 'atk')
        self.assertEqual(1, self.game.current_player.get_hand_size())
        self.assertEqual(self.player2_card2, self.game.current_player.monster_field[0])

    def test_attack_monster_attacker_loses(self):
        # summon monsters
        self.game.normal_summon(0, 'atk')
        self.game.change_turn()
        self.game.normal_summon(1, 'atk')
        self.game.change_turn()

        # player0 monster attacks player1 monster
        # lp lost will be abs(600 - 1200) = 600 and attacking monster will be destroyed
        # lp will be lost from attacking player
        self.game.attack_monster(0, 0)
        self.assertEqual(None, self.game.current_player.monster_field[0])
        self.assertNotEqual(None, self.game.other_player.monster_field[0])

        self.assertEqual(1, self.game.current_player.get_graveyard_size())
        self.assertEqual(0, self.game.other_player.get_graveyard_size())

        self.assertEqual(4400, self.game.current_player.life_points)
        self.assertEqual(5000, self.game.other_player.life_points)

    def test_attack_monster_attacker_ties(self):
        # summon monsters
        self.game.normal_summon(0, 'atk')
        self.game.change_turn()
        self.game.normal_summon(0, 'atk')
        self.game.change_turn()

        # player0 monster attacks player1 monster
        # lp lost will be abs(600 - 600) = 0 and both monsters will be destroyed
        self.game.attack_monster(0, 0)
        self.assertEqual(None, self.game.current_player.monster_field[0])
        self.assertEqual(None, self.game.other_player.monster_field[0])

        self.assertEqual(1, self.game.current_player.get_graveyard_size())
        self.assertEqual(1, self.game.other_player.get_graveyard_size())

        self.assertEqual(5000, self.game.current_player.life_points)
        self.assertEqual(5000, self.game.other_player.life_points)

    def test_attack_monster_attacker_wins(self):
        # summon monsters
        self.game.normal_summon(1, 'atk')
        self.game.change_turn()
        self.game.normal_summon(0, 'atk')
        self.game.change_turn()

        # player0 monster attacks player1 monster
        # lp lost will be abs(1200 - 600) = 600 and the targeted monster will be destroyed
        # lp will be lost from attacked player
        self.game.attack_monster(0, 0)
        self.assertNotEqual(None, self.game.current_player.monster_field[0])
        self.assertEqual(None, self.game.other_player.monster_field[0])

        self.assertEqual(0, self.game.current_player.get_graveyard_size())
        self.assertEqual(1, self.game.other_player.get_graveyard_size())

        self.assertEqual(5000, self.game.current_player.life_points)
        self.assertEqual(4400, self.game.other_player.life_points)

    def test_attack_directly(self):
        # summon monsters
        self.game.normal_summon(1, 'atk')
        self.game.change_turn()
        # skip second player's turn
        self.game.change_turn()

        self.game.attack_directly(0)

        # lp lost will be 1200, attacked player should now have 5000 - 1200 = 3800 lp left
        self.assertEqual(5000, self.game.current_player.life_points)
        self.assertEqual(3800, self.game.other_player.life_points)

    def test_attack_from_defense_position(self):
        self.game.normal_summon(1, 'def')
        self.game.change_turn()
        self.game.normal_summon(0, 'atk')
        self.game.change_turn()

        self.game.attack_monster(0, 0)

        # nothing should happen
        self.assertEqual(5000, self.game.current_player.life_points)
        self.assertEqual(5000, self.game.other_player.life_points)
        self.assertEqual(self.player1_card2, self.player1.monster_field[0])
        self.assertEqual(self.player2_card1, self.player2.monster_field[0])

    def test_attack_monster_in_defense_position_attacker_wins(self):
        self.game.normal_summon(1, 'atk')
        self.game.change_turn()
        self.game.normal_summon(0, 'def')
        self.game.change_turn()

        self.game.attack_monster(0, 0)

        # nothing should happen to life points
        self.assertEqual(5000, self.game.current_player.life_points)
        self.assertEqual(5000, self.game.other_player.life_points)

        # check monster field
        self.assertEqual(self.player1_card2, self.player1.monster_field[0])
        self.assertEqual(None, self.player2.monster_field[0])

        # check graveyard
        self.assertEqual([], self.player1.graveyard)
        self.assertEqual([self.player2_card1], self.player2.graveyard)

    def test_attack_monster_in_defense_position_attacker_loses(self):
        self.game.normal_summon(0, 'atk')
        self.game.change_turn()
        self.game.normal_summon(1, 'def')
        self.game.change_turn()

        self.game.attack_monster(0, 0)

        # nothing should happen to life points
        self.assertEqual(4600, self.game.current_player.life_points)
        self.assertEqual(5000, self.game.other_player.life_points)

        # check monster field
        self.assertEqual(self.player1_card1, self.player1.monster_field[0])
        self.assertEqual(self.player2_card2, self.player2.monster_field[0])

        # check graveyard
        self.assertEqual([], self.player1.graveyard)
        self.assertEqual([], self.player2.graveyard)

    def test_attack_directly_fails(self):
        # summon monsters
        self.game.normal_summon(1, 'atk')
        self.game.change_turn()
        self.game.normal_summon(1, 'atk')
        self.game.change_turn()

        self.game.attack_directly(0)

        # Nothing should happen since attacked player has monsters on their field
        self.assertEqual(5000, self.game.current_player.life_points)
        self.assertEqual(5000, self.game.other_player.life_points)

    def test_attack_directly_ends_game(self):
        # set life points for players
        self.player1.life_points = 1000
        self.player2.life_points = 1000

        # summon monsters
        self.game.normal_summon(1, 'atk')
        self.game.change_turn()
        # skip second player's turn
        self.game.change_turn()

        self.game.attack_directly(0)

        # attacked player will lose 1200 lp but since they only have 1000 lp their new total should be 0
        self.assertEqual(1000, self.game.current_player.life_points)
        self.assertEqual(0, self.game.other_player.life_points)
