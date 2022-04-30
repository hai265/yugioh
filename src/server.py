import json
import logging

import socket
from threading import Thread
import select
from src.game import GameController, GameStatus
from src.yugioh import Yugioh
from src.network import Network
from collections import defaultdict

"""

Code is adapted from https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/

"""

TCP_MAX = 65535


class YugiohServer:
    def __init__(self, server_ip: str, port: int):
        self.games: dict[int, list[GameController]] = {}
        self.id_count = 0
        self.id_to_sockets:dict[int, list[socket.socket]] = defaultdict(list)  # Dict that maps session_id to sockets associated with the game
        self.server_ip = server_ip
        self.port = port

    def threaded_client(self, session_id: int):
        """
        Thread that is associated with a client and receives data from it.
        It
        Args:
            client_sock: Socket that corresponds to the connected client
            session_id: Game id that client is associated with
            get_pickle: True if the client requested to get data by pickle
        """
        network = Network()
        while True:
            try:
                (client_sockets_read, client_sockets_write, _) = select.select(self.id_to_sockets[session_id], self.id_to_sockets[session_id], [])
                for client_sock in client_sockets_read:
                    data = network.recv_data(client_sock)
                    logging.info("Recieved data from " + str(client_sock.getpeername()))
                    if len(data) == 0:
                        # Close game session if one client disconnects
                        self.close_game_session(session_id)
                        return
                    data = json.loads(data)
                    if session_id in self.games:
                        game = self.games[session_id]
                        if not data:
                            # Client closes the connection
                            break
                        else:
                            if data["operation"] == "create":
                                send_data = game.create_game(data)
                                if len(game.game.players) == 2:
                                    self.games[session_id].game_status = GameStatus.ONGOING
                            elif data["operation"] == "read":
                                send_data = game.read_game(data)
                            elif data["operation"] == "update":
                                send_data = game.update_game(data)
                            elif data["operation"] == "delete":
                                send_data = game.delete_game(data)
                                if data.get("get_pickle", False):
                                    for client_sock in client_sockets_write:
                                        network.send_data(client_sock, send_data)
                                else:
                                    for client_sock in client_sockets_write:
                                        network.send_data(client_sock, json.dumps(send_data).encode("utf-8"))
                                break
                            else:
                                logging.warning("Invalid operation")
                            # Only send game to both players once both have been initialized
                            if game.game.game_status != GameStatus.WAITING:
                                if data.get("get_pickle", False):
                                    for client_sock in client_sockets_write:
                                        network.send_data(client_sock, send_data)
                                else:
                                    for client_sock in client_sockets_write:
                                        network.send_data(client_sock, json.dumps(send_data).encode("utf-8"))
                    else:
                        break
            except OSError as e:
                logging.error(e)
                break
        logging.info("Lost connection to " + str(client_sock))
        try:
            self.close_game_session(session_id)
        except KeyError:
            pass

    def initialize_server(self):
        network = Network()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server_socket.bind((self.server_ip, self.port))
        except socket.error as e:
            logging.error(e)

        server_socket.listen()
        logging.info("Waiting for a connection, Server Started")

        while True:
            client_connection, addr = server_socket.accept()
            logging.info(f'Connected to: {addr}')

            self.id_count += 1
            session_id = ((self.id_count - 1) // 2) + 1
            self.id_to_sockets[session_id].append(client_connection)
            if self.id_count % 2 == 1:
                self.games[session_id] = Yugioh()
                logging.info("Waiting for another player")
            else:
                logging.info("Another player joined. Checking if both players are connected...")
                if self.check_both_players_connected(self.id_to_sockets[session_id]):
                    logging.info(f"Creating game {session_id}")
                    for player in range(0, 2):
                        network.send_data(self.id_to_sockets[session_id][player], json.dumps({"player": player, "session_id": session_id}).encode('utf-8'))
                    new_client_thread = Thread(target=self.threaded_client, args=(session_id,))
                    new_client_thread.start()
                else:
                   logging.warning("One player disconnected while creating game") 
                    
    def check_both_players_connected(self, client_socks):
        """Send an alive message to both clients to make sure that they are still alive
            :param: client_socks - list of sockets to check connectivity
        """
        network = Network()
        both_players_connected = True
        try:
            for sock in client_socks:
                network.send_data(sock, json.dumps({"session_id": 0}).encode('utf-8'))
            for sock in list(client_socks):
                (read, _, _) = select.select([sock], [], [], 10)
                data = network.recv_data(sock)
                if not data:
                    sock.close()
                    logging.info(f"Client {sock} disconnected")
                    both_players_connected = False
                    client_socks.remove(sock)
                    self.id_count -= 1     
        except Exception as e:
            logging.warn(e)
            return False          
        return both_players_connected

    def close_game_session(self, session_id: int):
        """Closes a game session associated with a session id
        :param: session_id - Session id associated with a game
        """
        self.games[session_id].delete_game({"session_id": session_id})
        del self.games[session_id]
        for sock in self.id_to_sockets[session_id]:
            sock.close()
        del self.id_to_sockets[session_id]
        logging.info("Closing Game with id: " + str(session_id))

if __name__ == "__main__":
    server_ip = "0.0.0.0"
    port = 5555
    server = YugiohServer(server_ip, port)
    logging.getLogger().setLevel(logging.DEBUG)
    server.initialize_server()
