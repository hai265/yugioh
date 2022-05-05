# Class for a command line interface to control the yugioh yugioh_game
import json
import os
import pickle
import socket
from asyncio.log import logger

from src.card import create_deck_from_preset, deck_to_card_name_list, monster_card_to_string
from src.game import GameController, GameStatus
from src.network import Network
from src.account_menu import display_prompt


class NetworkCli:
    """
    Class that represents a yugioh client that connects to a yugioh server, using the command line
    """
    _phase = None

    def __init__(self, server_ip: str, port=5555):
        self.players = []
        self.yugioh_game: GameController = GameController(0)
        self.client_socket = None
        self.session_id = 0
        self.player_place = 0
        self.session_id = 0
        self.name = ""
        self.network = Network()
        self.server_ip = server_ip
        self.port = port
        self.num_rounds = 0

    def display_board(self):
        """
        Displays the yugioh_game board and the current player's hand to the command line
        Returns: None
        """
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        print("It is currently " + str(self.yugioh_game.get_current_player().name) + "'s turn" + " Round " + str(
            self.num_rounds))
        for player in self.yugioh_game.players:
            print("{} ({}) 's field:".format(player.name, player.life_points))
            print_str = ""
            for card in player.monster_field:
                if card:
                    print_str += monster_card_to_string(card) + " | "
                else:
                    print_str += "None | "
            print(print_str)
        print()
        print(
            self.yugioh_game.get_current_player().name + " cards in deck: " + str(
                len(self.yugioh_game.get_current_player().deck)))
        print(self.yugioh_game.get_current_player().name + " cards in graveyard: " + str(
            len(self.yugioh_game.get_current_player().graveyard)))
        print(self.yugioh_game.get_current_player().name + "'s hand: ", )
        for card in self.yugioh_game.get_current_player().hand:
            if card is None:
                print("None")
            else:
                print(monster_card_to_string(card))

    def start_game(self):
        """
        Starts an instance of a yugioh yugioh_game on the command line
        """
        self.name = input("Enter your name: ")
        # Initialize players
        self.yugioh_game = GameController()
        game_state = self.connect_to_server()
        preset_deck = create_deck_from_preset("sources/preset1")
        preset_deck = deck_to_card_name_list(preset_deck)
        self.player_place, self.session_id = game_state["player"], game_state["session_id"]
        logger.debug("Send Create Game")
        self.network.send_data(self.client_socket,
                               json.dumps(
                                   {"operation": "create", "session_id": self.session_id, "player_name": self.name,
                                    "deck": preset_deck, "get_pickle": True}).encode('utf-8'))
        data = self.network.recv_data(self.client_socket)
        self.yugioh_game = pickle.loads(data)
        while self.yugioh_game.game_status == GameStatus.WAITING:
            data = self.network.recv_data(self.client_socket)
            self.yugioh_game = pickle.loads(data)
        while GameStatus.ONGOING:
            self.num_rounds += 1
            if self.yugioh_game.current_player != self.player_place:
                self.setState(WaitPhase())
                self._phase.conduct_phase()
            if self.yugioh_game.game_status == GameStatus.ENDED:
                break
            self.setState(DrawPhase())
            while not isinstance(self._phase, EndPhase):
                if not self._phase.conduct_phase():
                    self.close_game()
                    return
            if self.yugioh_game.is_there_winner():
                break
            self._phase.conduct_phase()
        self.close_game()
        return

    def authenticate_user(self):
        """
        Prompts the user to log in or register
        :return:
        """
        user_info = display_prompt()
        self.name = user_info["name"]
        print("Welcome " + self.name + ", it's time to duel!")
    def connect_to_server(self) -> dict:
        """
        Connects to the game server.
        :return: The game state that the server has
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.port))
        # Keep recieving until get a session_id that is not 0
        while True:
            game_state = json.loads(self.network.recv_data(self.client_socket))
            if game_state["session_id"] != 0:
                logger.debug("Recieved game start message")
                break
            else:
                logger.debug("Recieved alive message")
            self.network.send_data(self.client_socket, json.dumps({"session_id": 0}).encode('utf-8'))
        return game_state

    def setState(self, phase: 'Phase'):
        self._phase = phase
        self._phase.context = self

    def send_data_and_update_game(self, data: dict):
        """
        Method that sends data to the server and recieves data back to update
        Args:
            data: data to send to the server
        """
        try:
            self.network.send_data(self.client_socket, json.dumps(data).encode("utf-8"))
            self.yugioh_game = pickle.loads(self.network.recv_data(self.client_socket))
        except socket.error:
            pass

    def close_game(self):
        """
        Sends a "delete" to the server and closes the client and game
        """
        self.yugioh_game.game_status = GameStatus.ENDED
        if self.yugioh_game.is_there_winner():
            self.yugioh_game.game_status = GameStatus.ENDED
            if self.yugioh_game.players[1].life_points <= 0:
                print(self.yugioh_game.players[0].name + " won!")
                self.send_data_and_update_game(
                    {"operation": "delete", "session_id": self.session_id, "get_pickle": True})
            elif self.yugioh_game.players[0].life_points <= 0:
                print(self.yugioh_game.players[1].name + " won!")
                self.send_data_and_update_game(
                    {"operation": "delete", "session_id": self.session_id, "get_pickle": True})
            else:
                print("Tie")
                self.send_data_and_update_game(
                    {"operation": "delete", "session_id": self.session_id, "get_pickle": True})
            self.send_data_and_update_game(
                {"operation": "delete", "session_id": self.session_id, "get_pickle": True})

    def main(self):
        """
        Method to start the main command line interface
        """
        self.authenticate_user()
        self.start_game()


class Phase:
    """
    Class that represents the various phases that a yugioh game can be at
    """

    @property
    def context(self) -> NetworkCli:
        return self._context

    @context.setter
    def context(self, context: NetworkCli) -> None:
        self._context = context

    def conduct_phase(self) -> bool:
        raise NotImplementedError


class DrawPhase(Phase):
    """
    Phase where the player draws a card
    """

    def conduct_phase(self) -> bool:
        self.context.send_data_and_update_game(
            {"operation": "update", "player": self._context.player_place, "session_id": self._context.session_id,
             "move": "draw_card", "args": [1], "get_pickle": True})
        self.context.display_board()
        self.context.setState(MainPhase())
        return True


class MainPhase(Phase):
    """
    Phase in which the player can summon cards, change battle positions of monsters, play spells
    """

    def conduct_phase(self) -> bool:
        while True:
            monster_to_summon = int(input("Choose a monster to summon to the field (0 to cancel)"))
            if monster_to_summon == 0:
                break
            what_summon = int(input("1 to normal summon, 2 to tribute summon (0 to cancel)"))
            if what_summon == 1:
                self.normal_summon(monster_to_summon)
            elif what_summon == 2:
                self.tribute_summon(monster_to_summon)
            else:
                break
            self.context.display_board()
        self.context.display_board()
        self.context.setState(BattlePhase())
        return True

    def normal_summon(self, monster_to_summon):
        position = int(input("1 to summon face up, 2 to summon face down (0 to cancel)"))
        if position == 0:
            return
        if position == 1:
            self.context.send_data_and_update_game(
                {"operation": "update", "session_id": self.context.session_id,
                 "move": "normal_summon", "args":
                     [monster_to_summon - 1], "get_pickle": True})
        elif position == 2:
            self.context.send_data_and_update_game(
                {"operation": "update", "session_id": self.context.session_id,
                 "move": "normal_set", "args":
                     [monster_to_summon - 1], "get_pickle": True})
            self.context.display_board()

    def tribute_summon(self, monster_to_summon):
        if monster_to_summon == 0:
            return
        monster_to_sacrifice1 = int(input("Choose a monster to sacrifice from your field"))
        monster_to_sacrifice2 = int(input("Choose a monster to sacrifice from your field"))
        self.context.send_data_and_update_game(
            {"operation": "update", "session_id": self.context.session_id,
             "move": "tribute_summon", "args":
                 [monster_to_summon - 1, monster_to_sacrifice1 - 1, monster_to_sacrifice2 - 1], "get_pickle": True})
        self.context.display_board()


class BattlePhase(Phase):
    """
    Phase where the player can attack monsters and the player
    """

    def conduct_phase(self) -> bool:
        attacking_monster = int(input("Choose a monster from your field (0 to go to end turn)"))
        while attacking_monster != 0 and not self.context.yugioh_game.is_there_winner():
            self.context.display_board()
            targeted_monster = int(input("Target a monster to attack (6 to attack player 0 to go to end turn)"))
            if targeted_monster == 0:
                break
            else:
                if targeted_monster == 6:
                    self.context.send_data_and_update_game(
                        {"operation": "update", "session_id": self.context.session_id,
                         "move": "attack_player", "args": [attacking_monster - 1],
                         "get_pickle": True})
                else:
                    self.context.send_data_and_update_game({"operation": "update", "move": "attack_monster", "args":
                                                           [attacking_monster - 1, targeted_monster - 1],
                                                            "get_pickle": True})
            self.context.display_board()
            if self.context.yugioh_game.is_there_winner():
                return False
            attacking_monster = int(input("Choose a monster from your field (6 to attack player, 0 to go to end "
                                          "turn)"))
        self.context.setState(EndPhase())
        return True


class EndPhase(Phase):
    """
    Phase where the player ends their turn
    """

    def conduct_phase(self) -> bool:
        self.context.send_data_and_update_game(
            {"operation": "update", "session_id": self.context.session_id, "move": "change_turn",
             "args": [], "get_pickle": True})
        self.context.display_board()
        self.context.setState(WaitPhase())
        return True


class WaitPhase(Phase):
    """
    Phase where the player waits while the other player plays
    :returns True if the game can proceed. False if the game ended
    """

    def conduct_phase(self) -> bool:
        while self.context.yugioh_game.current_player != self.context.player_place:
            print("It is not your turn yet")
            data = self.context.network.recv_data(self.context.client_socket)
            self.context.yugioh_game = pickle.loads(data)
            self.context.display_board()
            if self.context.yugioh_game.game_status == GameStatus.ENDED:
                return False
        self.context.num_rounds += 1
        self.context.setState(DrawPhase())
        return True


class Context:
    _state = None

    def __init__(self, state: Phase) -> None:
        self.setState(state)

    def setState(self, state: Phase):
        print(f"Context: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def doSomething(self):
        self._state.conduct_phase()
