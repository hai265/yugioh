import json
import multiprocessing
from time import sleep
from unittest import IsolatedAsyncioTestCase
import websockets
from src.server import initialize_server
from src.card import create_deck_from_preset

SERVER_IP = "167.172.152.60"
# SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

from src.network import Network

# SERVER_IP = "167.172.152.60"
SERVER_IP = "ws://localhost:5555/"
SERVER_PORT = 5555


class TestYugiohServer(IsolatedAsyncioTestCase):
    def setUp(self):
        self.preset_deck = create_deck_from_preset("sources/preset1")
        self.preset_deck_string_list = []
        for card in self.preset_deck:
            self.preset_deck_string_list.append(card.name)
        self.network = Network()
        self.process = multiprocessing.Process(target=initialize_server)
        self.process.start()
        self.sockets = []
        sleep(1)

    def tearDown(self):
        for sock in self.sockets:
            sock.close()
        self.process.terminate()

    async def create_game(self):
        self.sockets.append(await websockets.connect(SERVER_IP))
        self.sockets.append(await websockets.connect(SERVER_IP))
        player1 = json.loads(await self.sockets[0].recv())
        player2 = json.loads(await self.sockets[1].recv())
        self.assertEqual(player1["player"], 0)
        self.assertEqual(player2["player"], 1)
        self.session_id = player1["session_id"]
        await self.network.send_data(self.sockets[0],
                                     (json.dumps(
                                         {"operation": "create", "session_id": self.session_id, "player_name": "Yugi",
                                          "deck": self.preset_deck_string_list})
                                      .encode('utf-8')))
        await self.network.send_data(self.sockets[1],
                                     json.dumps(
                                         {"operation": "create", "session_id": self.session_id, "player_name": "Kaiba",
                                          "deck": self.preset_deck_string_list}).encode('utf-8'))

    async def test_yugioh_server_create_game(self):
        await self.create_game()
        create_game_state1 = json.loads(await self.sockets[0].recv())
        create_game_state2 = json.loads(await self.sockets[1].recv())
        create_game_state2 = json.loads(await self.sockets[1].recv())
        self.assertTrue(create_game_state2["players"][create_game_state2["current_player"]]["name"] == "Yugi")
        self.assertTrue(create_game_state2["players"][create_game_state2["other_player"]]["name"] == "Kaiba")

    async def test_yugioh_server_read_game(self):
        await self.create_game()
        create_game_state1 = json.loads(await self.network.recv_data(self.sockets[0]))
        create_game_state2 = json.loads(await self.network.recv_data(self.sockets[1]))
        create_game_state2 = json.loads(await self.sockets[1].recv())
        await self.network.send_data(self.sockets[0],
                                     (json.dumps({"operation": "read", "session_id": self.session_id})
                                      .encode('utf-8')))
        await self.network.send_data(self.sockets[1],
                                     (json.dumps({"operation": "read", "session_id": self.session_id}).encode('utf-8')))
        read_game_state1 = json.loads(await self.network.recv_data(self.sockets[0]))
        read_game_state2 = json.loads(await self.network.recv_data(self.sockets[1]))
        self.assertEqual(read_game_state1, read_game_state2)
        self.assertEqual(create_game_state2, read_game_state1)
        self.assertEqual(create_game_state2, read_game_state2)

    async def test_yugioh_server_delete_game(self):
        await self.create_game()
        create_game_state1 = json.loads(await self.network.recv_data(self.sockets[0]))
        create_game_state2 = json.loads(await self.network.recv_data(self.sockets[1]))
        create_game_state2 = json.loads(await self.sockets[1].recv())
        await self.network.send_data(self.sockets[0],
                                     json.dumps({"operation": "delete", "session_id": self.session_id}).encode("utf-8"))
        delete_game_data1 = json.loads(await self.network.recv_data(self.sockets[0]))
        delete_game_data2 = json.loads(await self.network.recv_data(self.sockets[1]))
        self.assertTrue(delete_game_data1["session_id"], create_game_state1["session_id"])
        self.assertTrue(delete_game_data2["session_id"], create_game_state2["session_id"])
