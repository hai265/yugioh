# Game manages the logic of the game, determines the winner of game if one player's health reaches 0,
# manages putting monsters on each player's field.
import random
from src.player import Player
from src.card import Monster


class GameController:
    def __init__(self, player1: Player, player2: Player, session_id=0):
        self.current_player = player1
        self.other_player = player2
        self.session_id = session_id

    def determine_first_player(self):
        """Sets starting turn order.
        """
        self.current_player, self.other_player = random.sample([self.current_player, self.other_player], 2)

    def change_turn(self):
        """Changes player turn.
        """
        self.current_player, self.other_player = self.other_player, self.current_player

    def attack_monster(self, attacking_monster: int, attacked_monster: int):
        """Conducts an attack from one of current player's monsters to one of other player's monsters.

        Args:
            attacking_monster: Index on the current player's field of the monster that is attacking. Must be in attack
                position.
            attacked_monster: Index on the other player's field of the monster that is being attacked.
        """
        atk_monster = self.current_player.monster_field[attacking_monster]
        if atk_monster.position == 'def':
            return

        target_monster = self.other_player.monster_field[attacked_monster]

        if target_monster.position == 'atk':
            atk_difference = atk_monster.attack_points - target_monster.attack_points

            if atk_difference > 0:
                self.other_player.decrease_life_points(atk_difference)
                self.other_player.send_card_to_graveyard(attacked_monster, -1)
            elif atk_difference == 0:
                self.current_player.send_card_to_graveyard(attacking_monster, -1)
                self.other_player.send_card_to_graveyard(attacked_monster, -1)
            elif atk_difference < 0:
                self.current_player.decrease_life_points(abs(atk_difference))
                self.current_player.send_card_to_graveyard(attacking_monster, -1)
        elif target_monster.position == 'def':
            atk_difference = atk_monster.attack_points - target_monster.defense_points

            if atk_difference > 0:
                self.other_player.send_card_to_graveyard(attacked_monster, -1)
            elif atk_difference == 0:
                pass
            elif atk_difference < 0:
                self.current_player.decrease_life_points(abs(atk_difference))

    def attack_directly(self, attacking_monster):
        """Conducts an attack from one of current player's monsters directly towards the other player's life points.

        Args:
            attacking_monster: Index on the current player's field of the monster that is attacking.
        """
        position = self.current_player.monster_field[attacking_monster].position

        if all([monster is None for monster in self.other_player.monster_field]) and position == 'atk':
            atk = self.current_player.monster_field[attacking_monster].attack_points
            self.other_player.decrease_life_points(atk)

    def is_there_winner(self):
        """Checks if either player has won. A player has won if their opponent's life_points have reached 0.

        Returns:
            True if either player's life point total is 0, False otherwise.
        """
        return self.current_player.life_points == 0 or self.other_player.life_points == 0

    def get_winner(self):
        """Returns the player that won the game or None if the game was tied.

        Should only be called after is_there_winner returns True.

        Returns:
            Player that won or None if there was a tie
        """
        if self.is_there_winner():
            if self.current_player.life_points > 0:
                return self.current_player
            elif self.other_player.life_points > 0:
                return self.other_player
            elif self.current_player.life_points == 0 and self.other_player.life_points == 0:
                return None

    def read_game(self):
        pass

    def normal_summon(self, hand_idx: int, position: str):
        """Summons monster from current_players's hand onto current_player's field.

        Args:
            hand_idx: index in current_player's hand of monster to summon
            position: Position to summon monster in.
        """
        field_idx = self.current_player.monster_field.index(None)
        self.current_player.normal_summon(hand_idx, field_idx, position)

    def tribute_summon_monster(self, hand_idx: int, tribute1_idx: int, tribute2_idx: int, position: str):
        """Tribute summon monster from current player's hand onto current player's field.

        Args:
            hand_idx: index in current_player's hand of monster to summon
            tribute1_idx: index in current_player's field of first tribute monster
            tribute2_idx: index in current_player's field of second tribute monster, only needed when summoning a
                level 7 or higher monster
            position: Position to summon monster in.
        """
        self.current_player.tribute_summon(hand_idx, tribute1_idx, tribute2_idx, position)
