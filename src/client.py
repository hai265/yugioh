# Class for a command line interface to control the yugioh yugioh_game
import json
import os
import pickle
import socket
from asyncio.log import logger
import inquirer
from inquirer import errors

from src.card import create_deck_from_preset, deck_to_card_name_list, monster_card_to_string, Monster, Card
from src.game import GameController, GameStatus
from src.network import Network
from src.account_menu import display_prompt
from src.database_functions import update_win_loss_draw


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
        if len(self.name) == 0:

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
        self.user_info = display_prompt()
        self.name = self.user_info["name"]
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
                update_win_loss_draw(self.name, "w")
                self.send_data_and_update_game(
                    {"operation": "delete", "session_id": self.session_id, "get_pickle": True})
            elif self.yugioh_game.players[0].life_points <= 0:
                print(self.yugioh_game.players[1].name + " won!")
                update_win_loss_draw(self.name, "l")
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
            self.context.display_board()
            questions = [
                inquirer.List('choice',
                              message="Choose your action",
                              choices=['Summon a monster', 'Go to Battle Phase'],
                              ),
            ]
            answers = inquirer.prompt(questions)
            if answers['choice'] == "Go to Battle Phase":
                break
            hand_choices = generate_monster_card_question(self.context.yugioh_game.get_current_player().hand)
            hand_choices.append(("Cancel", -1))
            questions = [
                inquirer.List('choice',
                              message="Choose a monster from your hand to summon",
                              choices=hand_choices,
                              ),
            ]

            monster_to_summon = inquirer.prompt(questions)["choice"]
            if monster_to_summon == -1:
                continue
            questions = [
                inquirer.List('choice',
                              message="Choose a summoning method summon",
                              choices=["Normal Summon", "Tribute Summon", "Cancel"],
                              ),
            ]
            what_summon = inquirer.prompt(questions)["choice"]
            if what_summon == "Normal Summon":
                self.normal_summon(monster_to_summon)
            elif what_summon == "Tribute Summon":
                self.tribute_summon(monster_to_summon)
            else:
                break
            self.context.display_board()
        self.context.display_board()
        self.context.setState(BattlePhase())
        return True

    def normal_summon(self, monster_to_summon):
        questions = [
            inquirer.List('choice',
                          message="Choose a position to summon",
                          choices=["Face Up", "Face Down", "Cancel"],
                          ),
        ]
        position = inquirer.prompt(questions)["choice"]
        if position == "Cancel":
            return
        if position == "Face Up":
            self.context.send_data_and_update_game(
                {"operation": "update", "session_id": self.context.session_id,
                 "move": "normal_summon", "args":
                     [monster_to_summon], "get_pickle": True})
        elif position == "Face Down":
            self.context.send_data_and_update_game(
                {"operation": "update", "session_id": self.context.session_id,
                 "move": "normal_set", "args":
                     [monster_to_summon], "get_pickle": True})
            self.context.display_board()

    def tribute_summon(self, monster_to_summon):
        if monster_to_summon == -1:
            return

        def validator(_, answers):
            if -1 in answers or len(answers) == 2:
                return True
            else:
                raise errors.ValidationError('', reason='You must select two monsters on the field to proceed.')

        monster_choices = generate_monster_card_question(self.context.yugioh_game.get_current_player().monster_field)
        monster_choices.append(("Cancel", -1))
        questions = [
            inquirer.Checkbox('choice',
                              message="Choose two monsters to sacrifice on your field. (Press space to select and enter to finalize)",
                              choices=monster_choices, validate=validator
                              ),
        ]
        monsters_to_sacrifice = inquirer.prompt(questions)["choice"]
        if len(monsters_to_sacrifice) == 0 or -1 in monsters_to_sacrifice:
            return
        self.context.send_data_and_update_game(
            {"operation": "update", "session_id": self.context.session_id,
             "move": "tribute_summon", "args":
                 [monster_to_summon, monsters_to_sacrifice[0], monsters_to_sacrifice[1]], "get_pickle": True})
        self.context.display_board()


class BattlePhase(Phase):
    """
    Phase where the player can attack monsters and the player
    """

    def conduct_phase(self) -> bool:
        while True:
            self.context.display_board()
            monster_choices = generate_monster_card_question(
                self.context.yugioh_game.get_current_player().monster_field)
            monster_choices.append(("End Phase", -1))

            questions = [
                inquirer.List('choice',
                              message="Choose a monster on your field",
                              choices=monster_choices),
            ]
            attacking_monster = inquirer.prompt(questions)["choice"]
            if attacking_monster == -1:
                break
            monster_choices = generate_monster_card_question(
                self.context.yugioh_game.get_other_player().monster_field)
            monster_choices.append(("Attack Player", len(self.context.yugioh_game.get_other_player().monster_field)))
            monster_choices.append(("Cancel", -1))
            questions = [
                inquirer.List('choice',
                              message="Choose a target",
                              choices=monster_choices),
            ]
            targeted_monster = inquirer.prompt(questions)["choice"]
            if targeted_monster == -1:
                break
            else:
                if targeted_monster == len(self.context.yugioh_game.get_current_player().monster_field):
                    self.context.send_data_and_update_game(
                        {"operation": "update", "session_id": self.context.session_id,
                         "move": "attack_player", "args": [attacking_monster],
                         "get_pickle": True})
                else:
                    self.context.send_data_and_update_game({"operation": "update", "move": "attack_monster", "args":
                        [attacking_monster, targeted_monster],
                                                            "get_pickle": True})
            self.context.display_board()
            if self.context.yugioh_game.is_there_winner():
                return False
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


def generate_monster_card_question(card_choices: list[Card]) -> list[tuple[str, int]]:
    """
    Generate a list of card questions for an inquiry
    :param card_choices: A list of cards
    :return: a
    """
    monster_choices = []
    for field_idx, card in enumerate(card_choices):
        if card is not None and isinstance(card, Monster):
            monster_choices.append((card.name, field_idx))
    return monster_choices
