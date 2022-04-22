import socket
import sys
import json
from src import game
from src.game import GameController
from src.player import Player
from src.card import Monster

from src import game_network_proxy
# Class for a command line interface to control the yugioh yugioh_game
import os


# Status codes:
# -1: invalid command sent
# 0: yugioh_game is not running or is over
# 1: valid input
def monster_card_to_string(card: dict):
    """
    :param: card: The card to convert to a string
    :return: A string in format {cardName} {attack}/{defense}
    """
    return "{cardName} {attack}/{defense}".format(cardName=card["name"], attack=card["attack_points"],
                                                  defense=card["name"])


class Client:
    def __init__(self):
        self.socket = None
        self.game = GameController()

    def display_board(self, board: dict):
        """
        Displays the yugioh_game and the current player's hand to the command line
        :arg: dictionary representing the state of the yugioh_game
        :return: None
        """
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        print("It is currently " + str(board["current_player"]["name"]) + "'s turn")
        for player in board["players"]:
            print("{} ({}) 's field:".format(player["name"], player["life_points"]))
            print_str = ""
            for card in player["field"]:
                if type(card) is dict:
                    print_str += monster_card_to_string(card) + " | "
                else:
                    print_str += "None | "
            print(print_str)
        print()
        print(board["current_player"]["name"] + " cards in deck: " + str(len(board["current_player"]["deck"])))
        print(
            board["current_player"]["name"] + " cards in graveyard: " + str(len(self["current_player"]["graveyard"])))
        print(board["current_player"]["name"] + "'s hand: ")
        for card in board["current_player"]["hand"]:
            if type(card) is not dict:
                print("None")
            else:
                print(monster_card_to_string(card))

    def start_client(self):
        host, port = "localhost", 9999
        name = input("Enter your name: ")
        self.game.players.append(Player(8000, name))
        data = json.dumps({"name": name})

        # Create a socket (SOCK_STREAM means a TCP socket)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            self.socket = sock
            sock.connect((host, port))
            sock.sendall(bytes(data + "\n", "utf-8"))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-8")

            print("Sent:     {}".format(data))
            print("Received: {}".format(received))

            while True:
                received = str(sock.recv(1024), "utf-8")
                data = json.loads(received)
                if data["status"] == 1:
                    break
        print("Running yugioh_game")

        # Initialize players
        while not self.game.is_there_winner():
            self.game.current_player.draw_card()
            self.display_board()
            print()
            while True:
                monster_to_summon = int(input("Choose a monster to summon to the field (0 to go to battle phase)"))
                if monster_to_summon == 0:
                    break
                if self.game.current_player.hand[monster_to_summon - 1] is None:
                    self.display_board()
                    print("Target is not valid")
                if monster_to_summon != 0:
                    self.game.summon_monster(monster_to_summon - 1)
                    self.display_board()
                    break
            attacking_monster = int(input("Choose a monster from your field (6 to attack hero, 0 to go to end turn)"))
            while attacking_monster != 0:
                if self.game.current_player.field[attacking_monster - 1] is None:
                    self.display_board()
                    print("Target is not valid")
                    attacking_monster = int(input("Choose a monster from your field (6 to attack hero, 0 to go to end "
                                                  "turn)"))
                else:
                    targeted_monster = int(input("Target a monster to attack (0 to go to end turn)"))
                    if targeted_monster == 0:
                        break
                    if self.game.other_player.field[targeted_monster - 1] is None:
                        self.display_board()
                        print("Target is not valid")
                    else:
                        self.game.attack_monster(attacking_monster - 1, targeted_monster - 1)
                    attacking_monster = int(input("Choose a monster from your field (6 to attack hero, 0 to go to end "
                                                  "turn)"))
            self.game.change_turn()
        if self.game.players[1].lifepoints < 0:
            print(self.game.players[0] + "won!")
        elif self.game.players[0].lifepoints < 0:
            print(self.game.players[1] + "won!")
        else:
            print("Tie")

    def request_from_server(self, command: int):
        """
        :param command: Int to send necessary information to server
        :return: json containing either board state or status -1 and error message
        """
        self.socket.sendall(bytes(command))
        # Receive data from the server and shut down
        return json.loads(self.socket.recv(1024))
