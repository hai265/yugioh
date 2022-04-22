# # Class for a command line interface to control the yugioh yugioh_game
# from src import yugioh_game
# from src.yugioh_game import GameController
# from src.player import Player
# from src.card import Monster
# import csv
# import os
#
#
# class Cli:
#     def __init__(self):
#         self.players = []
#         self.yugioh_game = None
#
#     def display_board(self):
#         """
#         Displays the yugioh_game board and the current player's hand to the command line
#         :return: None
#         """
#         if os.name == 'nt':
#             os.system('cls')
#         else:
#             os.system('clear')
#         print("It is currently " + str(self.yugioh_game.current_player.name) + "'s turn")
#         for player in self.yugioh_game.players:
#             print("{} ({}) 's field:".format(player.name, player.life_points))
#             print_str = ""
#             for card in player.field:
#                 if card:
#                     print_str += yugioh_game.monster_card_to_string(card) + " | "
#                 else:
#                     print_str += "None | "
#             print(print_str)
#         print()
#         print(self.yugioh_game.current_player.name + " cards in deck: " + str(len(self.yugioh_game.current_player.deck)))
#         print(self.yugioh_game.current_player.name + " cards in graveyard: " + str(len(self.yugioh_game.current_player.graveyard)))
#         print(self.yugioh_game.current_player.name + "'s hand: ",)
#         for card in self.yugioh_game.current_player.hand:
#             if card is None:
#                 print("None")
#             else:
#                 print(yugioh_game.monster_card_to_string(card))
#
#     def start_game(self):
#         """
#         Starts an instance of a yugioh yugioh_game on the command line
#         :return: None
#         """
#         # Initialize players
#         self.yugioh_game = GameController()
#         print("Enter the name of the first player")
#         name1 = input()
#         self.yugioh_game.players.append(Player(8000, name1))
#         print("Enter the name of the second player")
#         name2 = input()
#         self.yugioh_game.players.append(Player(8000, name2))
#         self.yugioh_game.current_player = self.yugioh_game.players[0]
#         self.yugioh_game.other_player = self.yugioh_game.players[1]
#
#         #   Initialize each player's deck
#         self.yugioh_game.players[0].deck = yugioh_game.create_deck_from_preset("sources/preset1")
#         self.yugioh_game.players[1].deck = yugioh_game.create_deck_from_preset("sources/preset1")
#         # Start each player off with 3 cards
#         for i in range(3):
#             self.yugioh_game.players[0].draw_card()
#             self.yugioh_game.players[1].draw_card()
#         #       Start the yugioh_game
#         while not self.yugioh_game.is_there_winner():
#             self.yugioh_game.current_player.draw_card()
#             self.display_board()
#             print()
#             while True:
#                 monster_to_summon = int(input("Choose a monster to summon to the field (0 to go to battle phase)"))
#                 if monster_to_summon == 0:
#                     break
#                 if self.yugioh_game.current_player.hand[monster_to_summon - 1] is None:
#                     self.display_board()
#                     print("Target is not valid")
#                 if monster_to_summon != 0:
#                     self.yugioh_game.summon_monster(monster_to_summon - 1)
#                     self.display_board()
#                     break
#             attacking_monster = int(input("Choose a monster from your field (6 to attack hero, 0 to go to end turn)"))
#             while attacking_monster != 0:
#                 if self.yugioh_game.current_player.field[attacking_monster - 1] is None:
#                     self.display_board()
#                     print("Target is not valid")
#                     attacking_monster = int(input("Choose a monster from your field (6 to attack hero, 0 to go to end "
#                                                   "turn)"))
#                 else:
#                     targeted_monster = int(input("Target a monster to attack (0 to go to end turn)"))
#                     if targeted_monster == 0:
#                         break
#                     if self.yugioh_game.other_player.field[targeted_monster - 1] is None:
#                         self.display_board()
#                         print("Target is not valid")
#                     else:
#                         self.yugioh_game.attack_monster(attacking_monster - 1, targeted_monster - 1)
#                     attacking_monster = int(input("Choose a monster from your field (6 to attack hero, 0 to go to end "
#                                                   "turn)"))
#             self.yugioh_game.change_turn()
#         if self.yugioh_game.players[1].lifepoints < 0:
#             print(self.yugioh_game.players[0] + "won!")
#         elif self.yugioh_game.players[0].lifepoints < 0:
#             print(self.yugioh_game.players[1] + "won!")
#         else:
#             print("Tie")
