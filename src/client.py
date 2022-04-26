# Class for a command line interface to control the yugioh yugioh_game
import json
import os
import pickle
import socket

from src.card import create_deck_from_preset, deck_to_card_name_list, monster_card_to_string
from src.game import GameController, GameStatus
from src.player import Player
from src.network import Network

class NetworkCli:
    def __init__(self):
        self.players = []
        self.yugioh_game = None
        self.client_socket = None
        self.session_id = 0
        self.player_place = 0
        self.session_id = 0
        self.name = ""
        self.network = Network()

    def display_board(self):
        """
        Displays the yugioh_game board and the current player's hand to the command line
        :return: None
        """
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        print("It is currently " + str(self.yugioh_game.get_current_player().name) + "'s turn")
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

    def send_data_and_update_game(self, data: dict):
        """
        Method that sends data to the server and recieves data back to update
        :param data: data to send to the server
        :return: None
        """
        try:
            self.network.send_data(self.client_socket, json.dumps(data).encode("utf-8"))
        except Exception as e:
            print(e)
        self.yugioh_game = pickle.loads(self.network.recv_data(self.client_socket))

    def start_game(self):
        """
        Starts an instance of a yugioh yugioh_game on the command line
        :return: None
        """
        # Initialize players
        self.yugioh_game = GameController()
        print("Enter your name")
        self.name = input()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 5555))
        game_state = json.loads(self.network.recv_data(self.client_socket,))
        preset_deck = create_deck_from_preset("sources/preset1")
        preset_deck = deck_to_card_name_list(preset_deck)
        self.player_place, self.session_id = game_state["player"], game_state["session_id"]
        self.network.send_data(self.client_socket, 
            json.dumps({"operation": "create", "session_id": self.session_id, "player_name": self.name,
                        "deck": preset_deck, "get_pickle": True}).encode('utf-8'))
        data = self.network.recv_data(self.client_socket)
        self.yugioh_game = pickle.loads(data)
        # Keep listening until game state changes to ONGOING
        print("Waiting for other player to connect...")
        while self.yugioh_game.game_status == GameStatus.WAITING:
            data = self.network.recv_data(self.client_socket)
            self.yugioh_game = pickle.loads(data)
        while self.yugioh_game.game_status == GameStatus.ONGOING:
            while True:
                self.display_board()
                # Wait until it is the player's turn
                while self.yugioh_game.current_player != self.player_place:
                    print("It is not your turn yet")
                    data = self.network.recv_data(self.client_socket)
                    self.yugioh_game = pickle.loads(data)
                    self.display_board()
                if self.yugioh_game.is_there_winner():
                    if self.yugioh_game.players[1].life_points <= 0:
                        print(self.yugioh_game.players[0].name + " won!")
                        self.yugioh_game.game_status = GameStatus.ENDED
                        self.send_data_and_update_game({"operation": "delete", "session_id": self.session_id,"get_pickle": True})
                    elif self.yugioh_game.players[0].life_points <= 0:
                        print(self.yugioh_game.players[1].name + " won!")
                        self.yugioh_game.game_status = GameStatus.ENDED
                        self.send_data_and_update_game({"operation": "delete", "session_id": self.session_id,"get_pickle": True})
                    else:
                        print("Tie")
                        self.yugioh_game.game_status = GameStatus.ENDED
                        self.send_data_and_update_game({"operation": "delete", "session_id": self.session_id,"get_pickle": True})
                    self.send_data_and_update_game({"operation": "delete", "session_id": self.session_id,"get_pickle": True})
                    return

                self.send_data_and_update_game({"operation": "update", "player":self.player_place, "session_id": self.session_id,
                                                "move": "draw_card", "args": [1], "get_pickle": True})
                self.display_board()
                monster_to_summon = int(input("Choose a monster to summon to the field (0 to go to battle phase)"))
                if monster_to_summon == 0:
                    break
                if monster_to_summon != 0:
                    self.send_data_and_update_game({"operation": "update", "session_id": self.session_id,
                                                    "move": "summon_monster", "args":
                                                    [monster_to_summon - 1, "atk"], "get_pickle": True})
                    self.display_board()
                    break
            attacking_monster = int(input("Choose a monster from your field (0 to go to end turn)"))
            while attacking_monster != 0 and not self.yugioh_game.is_there_winner():
                self.display_board()
                targeted_monster = int(input("Target a monster to attack (6 to attack player 0 to go to end turn)"))
                if targeted_monster == 0:
                    break
                else:
                    if targeted_monster == 6:
                        self.send_data_and_update_game({"operation": "update", "session_id": self.session_id,
                                                        "move": "attack_player", "args": [attacking_monster - 1],
                                                        "get_pickle": True})
                    else:
                        self.send_data_and_update_game({"operation": "update", "move": "attack_monster", "args":
                                                        [attacking_monster - 1, targeted_monster - 1],
                                                        "get_pickle": True})
                self.display_board()
                if self.yugioh_game.is_there_winner():
                    break
                attacking_monster = int(input("Choose a monster from your field (6 to attack player, 0 to go to end "
                                                "turn)"))
            if self.yugioh_game.is_there_winner():    
                if self.yugioh_game.players[1].life_points <= 0:
                    print(self.yugioh_game.players[0].name + " won!")
                    self.yugioh_game.game_status = GameStatus.ENDED
                    self.send_data_and_update_game({"operation": "delete", "session_id": self.session_id,"get_pickle": True})
                    self.send_data_and_update_game({"operation": "update", "session_id": self.session_id, "move": "change_turn",
                                            "args": [], "get_pickle": True})
                    break
                elif self.yugioh_game.players[0].life_points <= 0:
                    print(self.yugioh_game.players[1].name + " won!")
                    self.yugioh_game.game_status = GameStatus.ENDED
                    self.send_data_and_update_game({"operation": "delete", "session_id": self.session_id,"get_pickle": True})
                    self.send_data_and_update_game({"operation": "update", "session_id": self.session_id, "move": "change_turn",
                                            "args": [], "get_pickle": True})
                    break
                else:
                    print("Tie")
                    self.yugioh_game.game_status = GameStatus.ENDED
                    self.send_data_and_update_game({"operation": "delete", "session_id": self.session_id,"get_pickle": True})
                    self.send_data_and_update_game({"operation": "update", "session_id": self.session_id, "move": "change_turn",
                                            "args": [], "get_pickle": True})
                    break
            self.send_data_and_update_game({"operation": "update", "session_id": self.session_id, "move": "change_turn",
                                            "args": [], "get_pickle": True})
            
        
        
