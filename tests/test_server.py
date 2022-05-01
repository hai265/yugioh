from http import server
import json
import multiprocessing
import pickle
import socket
from time import sleep
import unittest

from src.card import create_deck_from_preset
from src.game import GameStatus
from src.network import Network
from src.server import YugiohServer

SERVER_IP = "167.172.152.60"
# SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

iom src.network import Network
from src.server import YugiohServer

SERVER_IP = "167.172.152.60"
# SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

@unittest.skiptest("skip server test")
class TestYugiohServer(unittest.TestCase):
    def setUp(self):
        self.preset_deck = create_deck_from_preset("sources/preset1")
        self.preset_deck_string_list = []
        for card in self.preset_deck:
            self.preset_deck_string_list.append(card.name)
        self.network = Network()
        self.sockets = []

    def tearDown(self):
        for sock in self.sockets:
            sock.close()

    def create_game(self):
        self.sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.sockets[0].connect((SERVER_IP, SERVER_PORT))
        self.sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.sockets[1].connect((SERVER_IP, SERVER_PORT))
        self.network.recv_data(self.sockets[0])
        self.network.send_data(self.sockets[0], json.dumps({"session_id": 0}).encode('utf-8'))
        self.network.recv_data(self.sockets[1])
        self.network.send_data(self.sockets[1], json.dumps({"session_id": 0}).encode('utf-8'))
        player1, self.session_id = json.loads(self.network.recv_data(self.sockets[0]))
        player2, self.session_id = json.loads(self.network.recv_data(self.sockets[1]))
        self.assertTrue(player1, 0)
        self.assertTrue(player2, 1)

        self.network.send_data(self.sockets[0],
                               (json.dumps({"operation": "create", "session_id": self.session_id, "player_name": "Yugi",
                                            "deck": self.preset_deck_string_list})
                                .encode('utf-8')))
        sleep(2)
        self.network.send_data(self.sockets[1],
                               json.dumps({"operation": "create", "session_id": self.session_id, "player_name": "Kaiba",
                                           "deck": self.preset_deck_string_list}).encode('utf-8'))

    def test_connect_to_yugioh_server(self):
        self.sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.sockets[0].connect((SERVER_IP, SERVER_PORT))
        self.sockets[1].connect((SERVER_IP, SERVER_PORT))
        data = self.network.recv_data(self.sockets[0])
        data = json.loads(data)
        self.assertTrue(data["session_id"] == 0)
        data = self.network.recv_data(self.sockets[1])
        data = json.loads(data)
        self.assertTrue(data["session_id"] == 0)

    def test_yugioh_server_create_game(self):
        self.create_game()
        self.network.send_data(self.sockets[1],
                               json.dumps({"operation": "create", "session_id": self.session_id, "player_name": "Kaiba",
                                           "deck": self.preset_deck_string_list}).encode('utf-8'))
        create_game_state1 = json.loads(self.network.recv_data(self.sockets[0]))
        create_game_state2 = json.loads(self.network.recv_data(self.sockets[1]))
        self.assertEqual(create_game_state1, create_game_state2)
        self.assertTrue(create_game_state2["players"][create_game_state2["current_player"]]["name"] == "Yugi")
        self.assertTrue(create_game_state2["players"][create_game_state2["other_player"]]["name"] == "Kaiba")

    def test_yugioh_server_read_game(self):
        self.create_game()
        create_game_state1 = json.loads(self.network.recv_data(self.sockets[0]))
        create_game_state2 = json.loads(self.network.recv_data(self.sockets[1]))
        self.network.send_data(self.sockets[0],
                               (json.dumps({"operation": "read", "session_id": self.session_id})
                                .encode('utf-8')))
        self.network.send_data(self.sockets[1],
                               (json.dumps({"operation": "read", "session_id": self.session_id}).encode('utf-8')))
        read_game_state1 = json.loads(self.network.recv_data(self.sockets[0]))
        read_game_state2 = json.loads(self.network.recv_data(self.sockets[1]))
        self.assertEqual(read_game_state1, read_game_state2)
        self.assertEqual(create_game_state2, read_game_state1)
        self.assertEqual(create_game_state2, read_game_state2)

    def test_yugioh_server_delete_game(self):
        self.create_game()
        create_game_state1 = json.loads(self.network.recv_data(self.sockets[0]))
        create_game_state2 = json.loads(self.network.recv_data(self.sockets[1]))
        self.network.send_data(self.sockets[0],
                               json.dumps({"operation": "delete", "session_id": self.session_id}).encode("utf-8"))
        delete_game_data1 = json.loads(self.network.recv_data(self.sockets[0]))
        delete_game_data2 = json.loads(self.network.recv_data(self.sockets[1]))
        self.assertTrue(delete_game_data1["session_id"], create_game_state1["session_id"])
        self.assertTrue(delete_game_data2["session_id"], create_game_state2["session_id"])

