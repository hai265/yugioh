import json
import multiprocessing
import pickle
import socket
import unittest

from src.card import create_deck_from_preset
from src.game import GameStatus
from src.server import initialize_server
from src.network import Network


@unittest.skip('tests not finished')
class TestYugiohServer(unittest.TestCase):
    def setUp(self):
        self.preset_deck = create_deck_from_preset("sources/preset1")
        self.preset_deck_string_list = []
        for card in self.preset_deck:
            self.preset_deck_string_list.append(card.name)
        self.process = multiprocessing.Process(target=initialize_server)
        self.process.start()
        self.network = Network()

    def tearDown(self):
        pass
        self.process.terminate()

    def test_connect_to_yugioh_server(self):
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect(("127.0.0.1", 5555))
        data = self.network.recv_data(sock1)
        data = json.loads(data)
        self.assertTrue(data["player"] == 0)
        self.assertTrue(data["session_id"] == 1)
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect(("127.0.0.1", 5555))
        data = self.network.recv_data(sock2)
        data = json.loads(data)
        self.assertTrue(data["player"] == 1)
        self.assertTrue(data["session_id"] == 1)
        sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock3.connect(("127.0.0.1", 5555))
        data = self.network.recv_data(sock3)
        data = json.loads(data)
        self.assertTrue(data["player"] == 0)
        self.assertTrue(data["session_id"] == 2)

    def test_yugioh_server_create_game(self):
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect(("127.0.0.1", 5555))
        data = self.network.recv_data(sock1)
        game_state = json.loads(data)
        player_place, session_id = game_state["player"], game_state["session_id"]
        self.network.send_data(sock1,
                               (json.dumps({"operation": "create", "session_id": session_id, "player_name": "Yugi",
                                            "deck": self.preset_deck_string_list})
                                .encode('utf-8')))
        game_state = json.loads(self.network.recv_data(sock1))
        self.assertTrue(game_state["session_id"] == 1)

        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect(("127.0.0.1", 5555))
        data = self.network.recv_data(sock2)
        player_place, session_id = json.loads(data)["player"], json.loads(data)["session_id"]
        self.network.send_data(sock2,
                               json.dumps({"operation": "create", "session_id": session_id, "player_name": "Kaiba",
                                           "deck": self.preset_deck_string_list}).encode('utf-8'))
        data = self.network.recv_data(sock2)
        game_state = json.loads(data)
        self.assertTrue(game_state["players"][game_state["current_player"]]["name"] == "Yugi")
        self.assertTrue(game_state["players"][game_state["other_player"]]["name"] == "Kaiba")

    def test_yugioh_server_read_game(self):
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect(("127.0.0.1", 5555))
        data = sock1.recv(8192)
        game_state = json.loads(data)
        player_place, session_id = game_state["player"], game_state["session_id"]
        sock1.sendall(json.dumps({"operation": "create", "session_id": session_id, "player_name": "Yugi",
                                  "deck": self.preset_deck_string_list})
                      .encode('utf-8'))
        game_state = json.loads(self.network.recv_data(sock1))
        sock1.sendall(json.dumps({"operation": "read", "session_id": session_id})
                      .encode('utf-8'))
        game_state2 = json.loads(self.network.recv_data(sock1))
        self.assertEqual(game_state, game_state2)

    def test_yugioh_server_delete_game(self):
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect(("127.0.0.1", 5555))
        data = self.network.recv_data(sock1)
        game_state = json.loads(data)
        player_place, session_id = game_state["player"], game_state["session_id"]
        sock1.sendall(json.dumps({"operation": "create", "session_id": session_id, "player_name": "Yugi",
                                  "deck": self.preset_deck_string_list})
                      .encode('utf-8'))
        game_state = json.loads(self.network.recv_data(sock1))
        sock1.sendall(json.dumps({"operation": "delete", "session_id": session_id})
                      .encode('utf-8'))
        data = self.network.recv_data(sock1)
        game_state = json.loads(data)
        self.assertTrue(game_state["session_id"] == session_id)

    # def test_yugioh_server_update_game_draw_card(self):
    #     sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     sock1.connect(("127.0.0.1", 5555))
    #     data = sock1.recv(8192)
    #     game_state = json.loads(data)
    #     player_place, session_id = game_state["player"], game_state["session_id"]
    #     sock1.sendall(json.dumps({"operation": "create", "session_id": session_id, "player_name": "Yugi",
    #                               "deck": self.preset_deck_string_list})
    #                   .encode('utf-8'))
    #     data = sock1.recv(8192)
    #     game_state = json.loads(data)
    #     sock1.sendall(json.dumps({"operation": "update", "session_id": session_id, "move": "draw_card",
    #                               "args": [1]})
    #                   .encode('utf-8'))
    #     game_state = json.loads(sock1.recv(8192))
    #     self.assertTrue(game_state["players"][0]["hand"][0]["name"] == "Hitotsu-Me Giant")


@unittest.skip('tests not finished')
class TestYugiohServerFeature(unittest.TestCase):
    def setUp(self):
        self.preset_deck = create_deck_from_preset("sources/preset1")
        self.preset_deck_string_list = []
        for card in self.preset_deck:
            self.preset_deck_string_list.append(card.name)
        self.process = multiprocessing.Process(target=initialize_server)
        self.process.start()

    def tearDown(self):
        pass
        self.process.terminate()
        self.network = Network()

    def test_create_game_send_data_to_both_students(self):
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect(("127.0.0.1", 5555))
        data = self.network.recv_data(sock1)
        game_state = json.loads(data)
        player_place, session_id = game_state["player"], game_state["session_id"]
        sock1.sendall(json.dumps({"operation": "create", "session_id": session_id, "player_name": "Yugi",
                                  "deck": self.preset_deck_string_list, "get_pickle": True})
                      .encode('utf-8'))
        game_state = pickle.loads(sock1.recv(4096))
        self.assertTrue(game_state.session_id == 1)
        self.assertTrue(game_state.game_status == GameStatus.WAITING)

        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect(("127.0.0.1", 5555))
        data = self.network.recv_data(sock2)
        player_place, session_id = json.loads(data)["player"], json.loads(data)["session_id"]
        sock2.sendall(json.dumps({"operation": "create", "session_id": session_id, "player_name": "Kaiba",
                                  "deck": self.preset_deck_string_list, "get_pickle": True})
                      .encode('utf-8'))
        game_state = pickle.loads(self.network.recv_data(sock1))
        self.assertTrue(game_state.session_id == 1)
        self.assertTrue(game_state.game_status == GameStatus.ONGOING)
        game_state = pickle.loads(self.network.recv_data(sock2))
        self.assertTrue(game_state.session_id == 1)
        self.assertTrue(game_state.game_status == GameStatus.ONGOING)

        sock1.sendall(json.dumps({"operation": "delete", "session_id": session_id, "get_pickle": True}).encode('utf-8'))
        game1 = pickle.loads(self.network.recv_data(sock1))
        game2 = pickle.loads(self.network.recv_data(sock2))
        self.assertEqual(game1.game_status, GameStatus.ENDED)
        self.assertEqual(game2.game_status, GameStatus.ENDED)
