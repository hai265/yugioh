# Class for a command line interface to control the yugioh game
from src.game import GameController
from src.player import Player
from src.card import Monster
import csv
import os


def create_card(card_name: str):
    """
        Args: card_name: The name of the card to be created
        Returns: a Card type corresponding to the card name, or None if no card exists with that name
    """
    with open('sources/cards.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0].lower().replace(" ", "") == card_name.lower().replace(" ", ""):
                return Monster(name=row[0], attribute=row[2], monster_type=row[3], level=int(row[4]),
                               attack_points=int(row[5]),
                               defense_points=int(row[6]), description=row[7])
        return None


def create_deck_from_preset(preset_path: str):
    """Method that creates a card object given the name of a card and returns it
        Args:
            preset_path: the path of the file that contains a card preset in csv
        Returns:
            a list containing Card objects
    """
    with open(preset_path, 'r') as csvfile:
        deck = []
        reader = csv.reader(csvfile)
        for row in reader:
            for name in row:
                deck.append(create_card(name))
        return deck


def monster_card_to_string(card: Monster):
    """
    :param: card: The card to convert to a string
    :return: A string in format {cardName} {attack}/{defense}
    """
    return "{cardName} {attack}/{defense}".format(cardName=card.name, attack=card.attackPoints,
                                                  defense=card.defensePoints)


class Cli:
    def __init__(self):
        self.players = []
        self.game = None

    def display_board(self):
        """
        Displays the game board and the current player's hand to the command line
        :return: None
        """
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        print("It is currently " + str(self.game.current_player.name) + "'s turn")
        for player in self.game.players:
            print("{} ({}) 's field:".format(player.name, player.life_points))
            print_str = ""
            for card in player.field:
                if card:
                    print_str += monster_card_to_string(card) + " | "
                else:
                    print_str += "None | "
            print(print_str)
        print()
        print(self.game.current_player.name + " cards in deck: " + str(len(self.game.current_player.deck)))
        print(self.game.current_player.name + " cards in graveyard: " + str(len(self.game.current_player.graveyard)))
        print(self.game.current_player.name + "'s hand: ",)
        for card in self.game.current_player.hand:
            if card is None:
                print("None")
            else:
                print(monster_card_to_string(card))

    def start_game(self):
        """
        Starts an instance of a yugioh game on the command line
        :return: None
        """
        # Initialize players
        self.game = GameController()
        print("Enter the name of the first player")
        name1 = input()
        self.game.players.append(Player(8000, name1))
        print("Enter the name of the second player")
        name2 = input()
        self.game.players.append(Player(8000, name2))
        self.game.current_player = self.game.players[0]
        self.game.other_player = self.game.players[1]

        #   Initialize each player's deck
        self.game.players[0].deck = create_deck_from_preset("sources/preset1")
        self.game.players[1].deck = create_deck_from_preset("sources/preset1")
        # Start each player off with 3 cards
        for i in range(3):
            self.game.players[0].draw_card()
            self.game.players[1].draw_card()
        #       Start the game
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