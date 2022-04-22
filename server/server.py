from src.game import GameController
from src.player import Player
from src.card import Monster
import csv
import json
import socket
from _thread import *
import pickle

"""

Code is adapted from https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/

"""


def connect_players():
    # Accept a connection, and recv for player information
    while len(server.player_sockets) < 2:
        connection, address = server.server_socket.accept()
        player_dict = json.loads(connection.recv(4096))
        server.player_sockets.append(connection)
        server.game.players.append(Player(8000, player_dict["name"]))


class YugiohServer:
    def __int__(self, server_ip: str, port: int):
        self.games = {}
        self.connected = set()
        self.id_count = 0
        self.server = server_ip
        self.port = 5555

    def threaded_client(self, client_sock: socket, player: int, game_id: int):
        """
        Thread that is associated with a client and receives data from it.
        It
        :param client_sock: Socket that corresponds to the connected client
        :param player: int to either 1st player or second player
        :param game_id: Game id that client is associated with
        :return: None
        """
        client_sock.send(str.encode(str(player)))
        while True:
            try:
                data = client_sock.recv(4096).decode()
                if game_id in self.games:
                    game = self.games[game_id]
                    if not data:
                        break
                    else:
                        if data == "reset":
                            game.delete_game()
                        elif data != "get":
                            game.update_game(data)
                        client_sock.sendall(pickle.dumps(game))
                else:
                    break
            except socket.error as e:
                print(e)
                break
        print("Lost connection")
        try:
            self.games[game_id].delete_game()
            del self.games[game_id]
            print("Closing Game", game_id)
        except KeyError as e:
            print(e)
            pass
        self.id_count -= 1
        client_sock.close()

    def __init__(self):
        self.player_sockets = []
        self.game = GameController()
        self.server_socket = socket.socket()

    def start_game(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server_sock.bind((self.server, self.port))
        except socket.error as e:
            str(e)

        server_sock.listen(2)
        print("Waiting for a connection, Server Started")

        while True:
            client_sock, client_addr = server_sock.accept()
            print("Connected to:", client_addr)
            self.id_count += 1
            player = 0
            game_id = (self.id_count - 1) // 2
            if self.id_count % 2 == 1:
                # TODO: Add gameid variable to GameController()
                self.games[game_id] = GameController()
                print("Creating a new yugioh_game...")
            else:
                self.games[game_id].ready = True
                player = 1
            start_new_thread(self.threaded_client, (client_sock, player, game_id))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = YugiohServer()
    server.server_socket.bind((HOST, PORT))

    connect_players()
    server.start_game()
