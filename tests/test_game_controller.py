import unittest
from src.card import create_card
from src.player import Player
from src.game import GameController


class TestGameController(unittest.TestCase):
    def setUp(self) -> None:
        # ATK for Curtain of the Dark One is 600 and ATK for Hitotsu-Me Giant 1200
        self.player0_card1 = create_card('Curtain of the Dark One')
        self.player0_card2 = create_card('Hitotsu-Me Giant')

        self.player1_card1 = create_card('Curtain of the Dark One')
        self.player1_card2 = create_card('Hitotsu-Me Giant')

        self.game = GameController()
        self.game.players.append(Player(5000, 'player0'))
        self.game.players.append(Player(5000, 'player1'))
        self.game.players[0].hand = [self.player0_card1, self.player0_card2]
        self.game.players[1].hand = [self.player1_card1, self.player1_card2]

        self.game.determine_first_player()

    def test_change_turns(self):
        self.game.change_turn()
        self.assertEqual(self.game.players[1], self.game.current_player)
        self.assertEqual(self.game.players[0], self.game.other_player)

    def test_summon_monsters(self):
        # player0 summon
        self.game.summon_monster(0)
        self.assertEqual(1, self.game.current_player.get_hand_size())
        self.assertEqual('Curtain of the Dark One', self.game.current_player.field[0].display_card()['name'])

        # change turn
        self.game.change_turn()

        # player1 summon
        self.game.summon_monster(1)
        self.assertEqual(1, self.game.current_player.get_hand_size())
        self.assertEqual('Hitotsu-Me Giant', self.game.current_player.field[0].display_card()['name'])

    def test_attack_monster_attacker_loses(self):
        # summon monsters
        self.game.summon_monster(0)
        self.game.change_turn()
        self.game.summon_monster(1)
        self.game.change_turn()

        # player0 monster attacks player1 monster
        # lp lost will be abs(600 - 1200) = 600 and attacking monster will be destroyed
        # lp will be lost from attacking player
        self.game.attack_monster(0, 0)
        self.assertEqual(None, self.game.current_player.field[0])
        self.assertNotEqual(None, self.game.other_player.field[0])

        self.assertEqual(1, self.game.current_player.get_graveyard_size())
        self.assertEqual(0, self.game.other_player.get_graveyard_size())

        self.assertEqual(4400, self.game.current_player.life_points)
        self.assertEqual(5000, self.game.other_player.life_points)

    def test_attack_monster_attacker_ties(self):
        # summon monsters
        self.game.summon_monster(0)
        self.game.change_turn()
        self.game.summon_monster(0)
        self.game.change_turn()

        # player0 monster attacks player1 monster
        # lp lost will be abs(600 - 600) = 0 and both monsters will be destroyed
        self.game.attack_monster(0, 0)
        self.assertEqual(None, self.game.current_player.field[0])
        self.assertEqual(None, self.game.other_player.field[0])

        self.assertEqual(1, self.game.current_player.get_graveyard_size())
        self.assertEqual(1, self.game.other_player.get_graveyard_size())

        self.assertEqual(5000, self.game.current_player.life_points)
        self.assertEqual(5000, self.game.other_player.life_points)

    def test_attack_monster_attacker_wins(self):
        # summon monsters
        self.game.summon_monster(1)
        self.game.change_turn()
        self.game.summon_monster(0)
        self.game.change_turn()

        # player0 monster attacks player1 monster
        # lp lost will be abs(1200 - 600) = 600 and the targeted monster will be destroyed
        # lp will be lost from attacked player
        self.game.attack_monster(0, 0)
        self.assertNotEqual(None, self.game.current_player.field[0])
        self.assertEqual(None, self.game.other_player.field[0])

        self.assertEqual(0, self.game.current_player.get_graveyard_size())
        self.assertEqual(1, self.game.other_player.get_graveyard_size())

        self.assertEqual(5000, self.game.current_player.life_points)
        self.assertEqual(4400, self.game.other_player.life_points)

