# Class for a command line interface to control the yugioh game
import random

from src.player import Player


class CLIInterface:
    def __init__(self):
        self.players = []
        self.currentPlayer = None

    def displaycurrentplayerhand(self):
        pass

    def set_current_player(self):
        pass

    def start_game(self):
        # Initalize players
        print("Enter the name of the first player")
        name1 = input()
        self.players.append(Player(8000, name1))
        print("Enter the name of the second player")
        name2 = input()
        self.players.append(Player(8000, name2))
        self.currentPlayer = self.players[random.randint(0, 1)]

#         Initialize each player's deck



