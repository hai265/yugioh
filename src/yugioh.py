import json
import pickle
from typing import Union, Any

from src.card import create_deck_from_array
from src.game import GameController, GameStatus
from src.player import Player


def to_dict(obj):
    """ Converts a yugioh yugioh_game session to a dictionary recursively
    """
    json_dict = json.loads(json.dumps(obj, default=lambda o: o.__dict__))
    return json_dict


def replace_game_property_values(game_dict):
    """
    Replace _current_player and _other_player with current_player and other_player
    Args:
        game_dict: Variable of all values related to game
    Returns: game_dict
    """
    return game_dict


class Yugioh:
    """ Yugioh is the yugioh_game interface in which the yugioh yugioh_game can be played by CRUD.
    """

    def __init__(self):
        self.game = GameController()
        self.current_turn = 1
        self.game_logger = GameLogger(self.game)

    def create_game(self, request: dict) -> Union[dict, bytes]:
        """

        Args:
            request: dictionary containing  key-value pairs. session_id: session id associated with the
                yugioh_game session. Within request we have:

                player_name: name of the player
                deck: a list of strings of card names to create the deck with
                player_place: whether the player is 1st place (0) or 2nd place (1). If not specified, will append
                get_pickle: optional false. If true, instead returns a pickled version of the game
        Returns: dict version of Game
        """
        player = Player(8000, name=request["player_name"])
        player.deck = create_deck_from_array(request["deck"])
        if "player_place" not in request:
            self.game.players.append(player)
        else:
            self.game.players.insert(request["player_place"], player)
        self.game.session_id = request["session_id"]
        if len(self.game.players) == 2:
            self.game.game_status = GameStatus.ONGOING
        if request.get('get_pickle', False):
            return pickle.dumps(self.game)
        return to_dict(self.game)

    def read_game(self, request: dict) -> Union[Union[list[str], bytes], Any]:
        """
        Args:
            request: dictionary containing single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing yugioh_game sessions.
            "get_game_actions": If true, then returns self.game_actions

        Returns:
            reply: dictionary containing a several key-value pairs that fully describe the yugioh_game's state.
        """
        if "get_game_actions" in request:
            return self.game_logger.get_logs()
        if request.get('get_pickle', False):
            return pickle.dumps(self.game)
        return to_dict(self.game)

    def update_game(self, request: dict) -> Union[bytes, Any]:
        """
        Args:
            request: dictionary describing the "move" to be made in the yugioh_game keys:
                session_id: value associated with a yugioh game session
                player: player to make the move as. 1 for player 1 or 2 for player 2
                move: Move to take in the yugioh game. Values can be , "summon_monster", "change_turn", "attack",
                "tribute_summon".
                args: a list of arguments needed to make the move

        Returns:
            dictionary describing the yugioh_game's new state.
        """
        if request["move"] == "attack_player":
            self.game_logger.log_action(request, self.current_turn)
            self.game.attack_player(*request["args"])
        if request["move"] == "change_turn":
            self.current_turn += 1
            self.game.change_turn()
        elif request["move"] == "draw_card":
            if "args" in request:
                self.game.players[request["player"]].draw_card(*request["args"])
            else:
                self.game.players[request["player"]].draw_card()
        elif request["move"] == "normal_summon":
            self.game_logger.log_action(request, self.current_turn)
            self.game.normal_summon(*request["args"])
        elif request["move"] == "normal_set":
            self.game_logger.log_action(request, self.current_turn)
            self.game.normal_set(*request["args"])
        elif request["move"] == "flip_summon":
            self.game_logger.log_action(request, self.current_turn)
            self.game.flip_summon(*request["args"])
        elif request["move"] == "tribute_summon":
            self.game_logger.log_action(request, self.current_turn)
            self.game.tribute_summon_monster(*request["args"])
        elif request["move"] == "attack_monster":
            self.game_logger.log_action(request, self.current_turn)
            self.game.attack_monster(*request["args"])
        elif request["move"] == "normal_spell":
            self.game_logger.log_action(request, self.current_turn)
            self.game.activate_spell(*request["args"])
        elif request["move"] == "equip_spell":
            self.game_logger.log_action(request, self.current_turn)
            self.game.equip_spell(*request["args"])

        if request.get('get_pickle', False):
            return pickle.dumps(self.game)

        return to_dict(self.game)

    def delete_game(self, request: dict) -> Union[dict, bytes]:
        """
        Args:
            request: dictionary containing a single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing yugioh_game sessions.

        Returns:
            dictionary containing a single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing yugioh_game sessions.
        """

        self.game.game_status = GameStatus.ENDED
        if request.get('get_pickle', False):
            return pickle.dumps(self.game)
        return to_dict(self.game)


class GameLogger:
    """
    Class that is responsible for recording game events
    Logs are in the format {"turn": turn, "player": player who took the action "message": log message} 
    """

    def __init__(self, game_controller: GameController) -> None:
        self.game_actions = []
        self.game_controller = game_controller

    def log_action(self, request: dict, turn: int):
        """
        Records game events into a list
        Args:
            request: a CRUD request to yugioh
            turn: turn where the action was taken
        """
        log = {"turn": turn, "player": self.game_controller.get_current_player().name}
        if request["move"] == "attack_monster":
            log["message"] = self.log_attack_monster_message(request)
        elif request["move"] == "normal_summon":
            log["message"] = self.log_normal_summon_message(request)
        elif request["move"] == "attack_player":
            log["message"] = self.log_attack_player_message(request)
        elif request["move"] == "tribute_summon":
            log["message"] = self.log_tribute_summon_message(request)
        elif request["move"] == "normal_spell":
            log["message"] = self.log_activate_spell_message(request)
        elif request["move"] == "equip_spell":
            log["message"] = self.log_activate_equip_spellmessage(request)
        elif request["move"] == "normal_set":
            log["message"] = self.log_normal_set_message(request)
        elif request["move"] == "flip_summon":
            log["message"] = self.log_flip_summon_message(request)
        self.game_actions.append(log)

    def log_normal_summon_message(self, request: dict) -> str:
        """
        Logs when a player normal summons a monster
        Args:
            request: a request to yugioh
        :returns
            a formatted log message
        """
        player = self.game_controller.get_current_player()
        summoned_monster = player.hand[request["args"][0]].name
        return f"{player.name} normal summoned {summoned_monster}"

    def log_attack_monster_message(self, request: dict) -> str:
        """
        Logs when a monster attacks a target. In format
        Args:
            request: a request to yugioh
        :returns
            a formatted log message
        """
        curr_player = self.game_controller.get_current_player()
        other_player = self.game_controller.get_other_player()
        attacking_monster = curr_player.monster_field[request["args"][0]].name
        attacked_monster = other_player.monster_field[request["args"][1]].name
        return f"{curr_player.name}'s {attacking_monster} attacked {other_player.name}'s {attacked_monster}"

    def log_attack_player_message(self, request: dict) -> str:
        """
        Logs when a monster attacks another monster. In format
        Args:
            request: a request to yugioh
        :returns
            a formatted log message
        """

        curr_player = self.game_controller.get_current_player()
        other_player = self.game_controller.get_other_player()
        attacking_monster = curr_player.monster_field[request["args"][0]].name
        return f"{curr_player.name}'s {attacking_monster} attacked {other_player.name} directly"

    def log_tribute_summon_message(self, request: dict) -> str:
        """
        Logs when a player tribute summons a monster from their hand. In format
        Args:
            request: a request to yugioh
        :returns
            a formatted log message
        """
        curr_player = self.game_controller.get_current_player()
        summoned_monster = curr_player.hand[request["args"][0]].name
        sacrificed1 = curr_player.monster_field[request["args"][1]].name
        sacrificed2 = curr_player.monster_field[request["args"][2]].name
        return f"{curr_player.name} tribute summoned {summoned_monster} by sacrificing {sacrificed1} and {sacrificed2}"

    def log_tribute_summon_message(self, request: dict) -> str:
        """
        Logs when a player tribute summons a monster from their hand. In format
        Args:
            request: a request to yugioh
        :returns
            a formatted log message
        """
        curr_player = self.game_controller.get_current_player()
        summoned_monster = curr_player.hand[request["args"][0]].name
        sacrificed1 = curr_player.monster_field[request["args"][1]].name
        sacrificed2 = curr_player.monster_field[request["args"][2]].name
        return f"{curr_player.name} tribute summoned {summoned_monster} by sacrificing {sacrificed1} and {sacrificed2}"

    def log_activate_spell_message(self, request) -> str:
        """
        Logs when a player activates a spell
            request: a request to yugioh
        :returns
            a formatted log message
        """
        player = self.game_controller.get_current_player()
        played_spell = player.hand[request["args"][0]].name
        return f"{player.name} played spell {played_spell}"

    def log_activate_equip_spellmessage(self, request) -> str:
        """
        Logs when a player activates an equip spell
            request: a request to yugioh
        :returns
            a formatted log message
        """
        curr_player = self.game_controller.get_current_player()
        spell = curr_player.hand[request["args"][1]].name
        targeted_monster = curr_player.monster_field[request["args"][0]]
        return f"{curr_player.name} used {spell} on {targeted_monster.name}"
    
    def log_normal_set_message(self, request) -> str:
        """
        Logs when a player summons a monster face down
            request: a request to yugioh
        :returns
            a formatted log message
        """
        player = self.game_controller.get_current_player()
        summoned_monster = player.hand[request["args"][0]].name
        return f"{player.name} summoned {summoned_monster} face down"

    def log_flip_summon_message(self, request) -> str:
        """
        Logs when a player summons a monster face down
            request: a request to yugioh
        :returns
            a formatted log message
        """
        player = self.game_controller.get_current_player()
        summoned_monster = player.monster_field[request["args"][0]].name
        return f"{player.name} flipped summoned {summoned_monster}"
