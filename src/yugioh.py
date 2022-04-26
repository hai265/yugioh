import json
import pickle

from src.game import GameController, GameStatus
from src.player import Player
from src.card import Monster, create_deck_from_array
from typing import Union, Any


def to_dict(obj):
    """ Converts a yugioh yugioh_game session to a dictionary recursively
    """
    json_dict = json.loads(json.dumps(obj, default=lambda o: o.__dict__))
    return json_dict


def replace_game_property_values(game_dict):
    """
    Replace _current_player and _other_player with current_player and other_player
    :param game_dict:
    :return: game_dict
    """
    return game_dict


class Yugioh:
    """ Yugioh is the yugioh_game interface in which the yugioh yugioh_game can be played by CRUD.
    """

    def __init__(self):
        self.game = GameController()

    def create_game(self, request: dict) -> Union[dict, bytes]:
        """

        :param request: dictionary containing  key-value pairs. session_id: session id associated with the
        yugioh_game session.
        'player_name': name of the player
        'deck' a list of strings of card names to create the deck with
        'get_pickle' optional false. If true, instead returns a pickled version of the game
        :return: dict version of Game
        """
        player = Player(8000, name=request["player_name"])
        player.deck = create_deck_from_array(request["deck"])
        self.game.players.append(player)
        self.game.session_id = request["session_id"]
        if len(self.game.players) == 2:
            self.game.game_status = GameStatus.ONGOING
        if request.get('get_pickle', False):
            return pickle.dumps(self.game)
        return replace_game_property_values(to_dict(self.game))

    def read_game(self, request: dict) -> Union[dict, bytes]:
        """
        Args:
            request: dictionary containing single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing yugioh_game sessions.

        Returns:
            reply: dictionary containing a several key-value pairs that fully describe the yugioh_game's state.
        """
        if request.get('get_pickle', False):
            return pickle.dumps(self.game)
        json_dict = to_dict(self.game)
        return json_dict

    def update_game(self, request: dict) -> dict:
        """
        Args:
            request: dictionary describing the "move" to be made in the yugioh_game keys:
            :arg: "session_id": value associated with a yugioh game session
            "player": player to make the move as. 1 for player 1 or 2 for player 2
            "move": Move to take in the yugioh game. Values can be , "summon_monster", "change_turn", "attack",
            "tribute_summon".
            "args": a list of arguments needed to make the move

        Returns:
            reply: dictionary describing the yugioh_game's new state.
        """
        if request["move"] == "attack_player":
            self.game.attack_player(*request["args"])
        if request["move"] == "change_turn":
            self.game.change_turn()
        elif request["move"] == "draw_card":
            if "args" in request:
                self.game.players[request["player"]].draw_card(*request["args"])
            else:
                self.game.players[request["player"]].draw_card()
        elif request["move"] == "summon_monster":
            self.game.normal_summon(*request["args"])
        elif request["move"] == "tribute_summon":
            self.game.tribute_summon_monster(*request["args"])
        elif request["move"] == "attack_monster":
            self.game.attack_monster(*request["args"])

        if request.get('get_pickle', False):
            return pickle.dumps(self.game)
        json_dict = to_dict(self.game)
        return replace_game_property_values(to_dict(self.game))

    def delete_game(self, request: dict) -> Union[dict, bytes]:
        """
        Args:
            request: dictionary containing a single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing yugioh_game sessions.

        Returns:
            reply: dictionary containing a single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing yugioh_game sessions.
        """

        self.game.game_status = GameStatus.ENDED
        if request.get('get_pickle', False):
            return pickle.dumps(self.game)
        json_dict = to_dict(self.game)
        return replace_game_property_values(to_dict(self.game))
