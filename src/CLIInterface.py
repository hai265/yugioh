# Class for a command line interface to control the yugioh game
import random

from src.game import GameController
from src.player import Player
from src.card import Monster
import csv


def create_card(card_name: str, ):
    """Returns an array of Card objects which are created using the names in a preset file"""
    with open('sources/cards.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0].lower().replace(" ", "") == card_name.lower().replace(" ", ""):
                return Monster(name=row[0], attribute=row[2], monster_type=row[3], level=row[4],
                               attackpoints=int(row[5]),
                               defensepoints=int(row[6]), description=row[7])
        return None


def create_deck_from_preset(preset_path: str):
    """Method that creates a card object given the name of a card and returns it"""
    with open(preset_path, 'r') as csvfile:
        deck = []
        reader = csv.reader(csvfile)
        for row in reader:
            for name in row:
                deck.append(create_card(name))
        return deck


class CLIInterface:
    def __init__(self):
        self.players = []
        self.currentPlayer = None
        self.game = None

    def display_current_player_hand(self):
        pass

    def set_current_player(self):
        pass

    def start_game(self):
        # Initialize players
        self.game = GameController()
        print("Enter the name of the first player")
        name1 = input()
        self.game.players.append(Player(8000, name1))
        print("Enter the name of the second player")
        name2 = input()
        self.game.players.append(Player(8000, name2))
        self.game.currentPlayer = self.game.players[random.randint(0, 1)]

        #         Initialize each player's deck
        self.game.players[0].deck = create_deck_from_preset("sources/preset1")
        self.game.players[1].deck = create_deck_from_preset("sources/preset1")
        # Start each player off with 3 cards
        for i in range(3):
            self.game.players[0].draw_card()
            self.game.players[1].draw_card()
        #       Start the game
        while not self.game.is_there_winner():
            print("It is currently " + str(self.game.currentPlayer) + "'s turn")
            self.game.currentPlayer.draw_card()
            print(self.game.currentPlayer.name + "'s hand: " + str(self.game.currentPlayer.hand))
            print(self.game.currentPlayer.name + "'s field: " + str(self.game.currentPlayer.field))
            monster_to_summon = int(input("Choose a monster to summon to the field (0 to go to battle phase)"))
            if monster_to_summon != 0:
                self.game.summon_monster(monster_to_summon - 1)
            attacking_monster = int(input("Target a monster (0 to go to end turn)"))
            if attacking_monster != 0:
                targeted_monster = int(input("Target a monster to attack (0 to go to end turn)"))
                if targeted_monster != 0:
                    self.game.attack_monster(attacking_monster - 1, targeted_monster - 1)
            self.game.change_turn()
        if self.game.players[1].lifepoints < 0:
            print(self.game.players[0] + "won!")
        elif self.game.players[0].lifepoints < 0:
            print(self.game.players[1] + "won!")
        else:
            print("Tie")
