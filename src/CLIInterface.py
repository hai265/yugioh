# Class for a command line interface to control the yugioh game
import random

from src.game import Game
from src.player import Player
from src.card import Card
from src.card import Monster
import csv


class CLIInterface:
    def __init__(self):
        self.players = []
        self.currentPlayer = None
        self.game = None

    def displaycurrentplayerhand(self):
        pass

    def set_current_player(self):
        pass

    def start_game(self):
        # Initalize players
        self.game = Game()
        print("Enter the name of the first player")
        name1 = input()
        self.game.players.append(Player(8000, name1))
        print("Enter the name of the second player")
        name2 = input()
        self.game.players.append(Player(8000, name2))
        self.game.currentPlayer = self.players[random.randint(0, 1)]

        #         Initialize each player's deck
        self.game.players[0] = self.create_deck_from_preset("preset1")
        self.game.players[1] = self.create_deck_from_preset("preset1")

    """Method that creates a card object given the name of a card and returns it"""

    def create_card(self, card_name: str, ):
        with open('sources/cards.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0].lower() == card_name.lower():
                    return Monster(name=row[0], card_type=row[1], attribute=row[2], type=row[3], level=row[4],
                                   attackpoints=row[5],
                                   defensepoints=row[6])

    """Returns an array of Card objects which are created using the names in a preset file"""

    def create_deck_from_preset(self, preset_path: str):
        with open(preset_path, 'r') as csvfile:
            deck = []
            reader = csv.reader(csvfile)
            for row in reader:
                for name in row:
                    deck.append(self.create_card(name))
            return deck
