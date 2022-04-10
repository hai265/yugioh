# Game manages the logic of the game, determines the winner of game if one player's health reaches 0,
# manages putting monsters on each player's field.
import random


class Game:
    def __init__(self):
        self.players = []
        self.current_player = None
        self.other_player = None
        self.field = []

    def determine_first_player(self):
        """
        Sets starting turn order.
        """
        # TODO: randomize starting turn order
        self.current_player = self.players[0]
        self.other_player = self.players[1]

    def change_turn(self):
        """
        Changes player turn
        """
        self.current_player, self.other_player = self.other_player, self.current_player

    def attack_monster(self, attacking_monster, attacked_monster):
        """
        Conducts an attack from attacking_monster onto attacked_monster
        :param attacking_monster: Monster that is attacking
        :param attacked_monster: Monster that is being attacked

        Note: Currently attacking only supports dealing with monster in attack position.
        """
        atk_monster = self.current_player.field[attacking_monster]
        target_monster = self.other_player.field[attacked_monster]
        atk_difference = atk_monster.attackPoints - target_monster.attackPoints

        if atk_difference > 0:
            self.other_player.decrease_life_points(atk_difference)
            self.other_player.send_card_to_graveyard(attacked_monster, -1)
        elif atk_difference == 0:
            self.current_player.send_card_to_graveyard(attacking_monster, -1)
            self.other_player.send_card_to_graveyard(attacked_monster, -1)
        elif atk_difference < 0:
            self.current_player.decrease_life_points(atk_difference)
            self.current_player.send_card_to_graveyard(attacking_monster, -1)

    def is_there_winner(self):
        """
        Checks if either player has won. A player has won if their opponent's life_points have reached 0.
        """
        return self.players[0].life_points == 0 or self.players[1].life_points == 0

    def read_game(self):
        pass

    def summon_monster(self, hand_idx, field_idx):
        """
        Summons monster from  current_players's hand onto current_player's field
        :param hand_idx: index in current_player's hand of monster to summon
        :param field_idx: index on field to where monster will be summoned to

        Note: Currently summoning only supports summoning monsters in attack position.
        """
        self.current_player.summon_mosnter(hand_idx, field_idx)

    def tribute_summon_monster(self):
        pass
