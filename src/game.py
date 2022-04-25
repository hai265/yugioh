# Game manages the logic of the yugioh_game, determines the winner of yugioh_game if one player's health reaches 0,
# manages putting monsters on each player's field.
from enum import IntEnum
from src.player import Player


class GameStatus(IntEnum):
    """
    Enum for representing the state of the yugioh game
    WAITING: Game has not started yet since another player is needed to connect
    ONGOING: Yugioh game is currently ongoing
    ENDED: Yugioh game has ended
    """
    WAITING = 1
    ONGOING = 2
    ENDED = 3


class GameController:
    def __init__(self, session_id=0, game_data=None):
        if game_data is None:
            self.players = []
            self.current_player = 0
            self.other_player = 1
            self.session_id = session_id
            self.game_status = GameStatus.WAITING
        else:
            self.players = [Player(game_data["players"][0]["life_points"], game_data["players"][0]["name"]),
                            Player(game_data["players"][1]["life_points"], game_data["players"][1]["name"])]
            self.current_player = game_data["current_player"]
            self.other_player = game_data["other_player"]
            self.session_id = game_data["session_id"]
            self.game_status = game_data["session_id"]

        # self.field = [None for _ in range(5)]

    def determine_first_player(self):
        """
        Sets starting turn order. Also sets game_staus to ONGOING
        """
        # TODO: randomize starting turn order
        self.current_player = 0
        self.other_player = 1
        self.game_status = GameStatus.ONGOING

    def change_turn(self):
        """
        Changes player turn
        """
        self.current_player, self.other_player = self.other_player, self.current_player

    def attack_monster(self, attacking_monster: int, attacked_monster: int):
        """
        Conducts an attack from attacking_monster onto attacked_monster
        :param attacking_monster: field_idx of monster that is attacking
        :param attacked_monster: field_idx of monster that is being attacked

        Note: Currently attacking only supports dealing with monster in attack position.
        """
        atk_monster = self.get_current_player().field[attacking_monster]
        target_monster = self.get_other_player().field[attacked_monster]
        atk_difference = atk_monster.attack_points - target_monster.attack_points

        if atk_difference > 0:
            self.get_other_player().decrease_life_points(atk_difference)
            self.get_other_player().send_card_to_graveyard(attacked_monster, -1)
        elif atk_difference == 0:
            self.get_current_player().send_card_to_graveyard(attacking_monster, -1)
            self.get_other_player().send_card_to_graveyard(attacked_monster, -1)
        elif atk_difference < 0:
            self.get_current_player().decrease_life_points(abs(atk_difference))
            self.get_current_player().send_card_to_graveyard(attacking_monster, -1)

    def is_there_winner(self):
        """
        Checks if either player has won. A player has won if their opponent's life_points have reached 0.
        """
        if self.players[0].life_points <= 0 or self.players[1].life_points <= 0:
            self.game_status = GameStatus.ENDED

    def read_game(self):
        pass

    def summon_monster(self, hand_idx: int):
        """
        Summons monster from  current_players's hand onto current_player's field
        :param hand_idx: index in current_player's hand of monster to summon

        Note: Currently summoning only supports summoning monsters in attack position.
        """
        field_idx = self.get_current_player().field.index(None)
        self.get_current_player().summon_monster(hand_idx, field_idx)

    def tribute_summon_monster(self):
        pass

    def get_current_player(self):
        return self.players[self.current_player]

    def get_other_player(self):
        return self.players[self.other_player]
