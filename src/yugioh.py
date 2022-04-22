import json

from src.game import GameController
from src.player import Player
from src.card import Monster, create_deck_from_array
import csv
import os


def to_dict(obj):
    """ Converts a yugioh yugioh_game session to a dictionary recursively
    """
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


class Yugioh:
    """ Yugioh is the yugioh_game interface in which the yugioh yugioh_game can be played by CRUD.
    """

    def __init__(self):
        self.game = GameController()

    def create_game(self, request: dict) -> dict:
        """

        :param request: dictionary containing  key-value pairs. session_id: session id associated with the
        yugioh_game session.
        'player_name': name of the player
        'deck' a list of strings of card names to create the deck with
        :return: dict version of Game
        """
        player = Player(5000, name=request["player_name"])
        player.deck = create_deck_from_array(request["deck"])
        self.game.players.append(player)
        self.game.session_id = request["session_id"]
        if len(self.game.players) == 2:
            self.game.determine_first_player()
        return to_dict(self.game)

    def read_game(self, request: dict) -> dict:
        """
        Args:
            request: dictionary containing single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing yugioh_game sessions.

        Returns:
            reply: dictionary containing a several key-value pairs that fully describe the yugioh_game's state.
        """
        return to_dict(self.game)

    def update_game(self, request: dict) -> dict:
        """
        Args:
            request: dictionary describing the "move" to be made in the yugioh_game keys:
            :arg: "session_id": value assosiated with a yugioh game session
            "player": player to make the move as. 1 for player 1 or 2 for player 2
            "move": Move to take in the yugioh game. Values can be , "summon_monster", "change_turn", "attack",
            "tribute_summon".
            "args": a list of arguments needed to make the move

        Returns:
            reply: dictionary describing the yugioh_game's new state.
        """
        raise NotImplementedError

    def delete_game(self, request: dict) -> dict:
        """
        Args:
            request: dictionary containing a single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing yugioh_game sessions.

        Returns:
            reply: dictionary containing a single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing yugioh_game sessions.
        """
        raise NotImplementedError
