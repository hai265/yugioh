import json
import logging

import socket
from threading import Thread
import select
from src.game import GameStatus
from src.yugioh import Yugioh
from src.network import Network


"""

Code is adapted from https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/

"""

TCP_MAX = 65535
class YugiohServer:
    def __init__(self, server_ip: str, port: int):
        self.games = {}
        self.connected = set()
        self.id_count = 0
        self.id_to_sockets = {}  # Dict that maps session_id to sockets associated with the game
        self.server = server_ip
        self.port = port

    def threaded_client(self, session_id: int):
        """
        Thread that is associated with a client and receives data from it.
        It
        :param client_sock: Socket that corresponds to the connected client
        :param session_id: Game id that client is associated with
        :param get_pickle: True if the client requested to get data by pickle
        :return: None
        """
        network = Network()
        while True:
            try:
                (client_sockets_read, client_sockets_write, _) = select.select(self.id_to_sockets[session_id], self.id_to_sockets[session_id], [])
                for client_sock in client_sockets_read:
                    data = network.recv_data(client_sock)
                    logging.info("Recieved data from " + str(client_sock.getpeername()))
                    if len(data) == 0:
                        # pop socket that disconnected
                        for sock in self.id_to_sockets[session_id]:
                            if sock == client_sock:
                                self.id_to_sockets[session_id].remove(sock)
                                logging.info(f"Client {client_sock.getpeername()} disconnected")

                        break
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
            self.games[session_id].delete_game({"session_id": session_id})
            del self.games[session_id]
            del self.id_to_sockets[session_id]
            logging.info("Closing Game with id: " + str(session_id))
        except KeyError:
            pass
        self.id_count -= 1
        client_sock.close()


def initialize_server():
    server_ip = "127.0.0.1"
    port = 5555
    yugioh_server = YugiohServer(server_ip, port)
    network = Network()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((server_ip, port))
    except socket.error as e:
        logging.error(e)

    server_socket.listen()
    logging.info("Waiting for a connection, Server Started")

    while True:
        client_connection, addr = server_socket.accept()
        logging.info(f'Connected to: {addr}')

        yugioh_server.id_count += 1
        player = 0
        session_id = ((yugioh_server.id_count - 1) // 2) + 1
        if yugioh_server.id_count % 2 == 1:
            yugioh_server.games[session_id] = Yugioh()
            yugioh_server.id_to_sockets[session_id] = [client_connection]
            logging.info("Waiting for another player")
        else:
            logging.info("Another player joined. Creating a new game...")
            player = 1
            yugioh_server.id_to_sockets[session_id].append(client_connection)
            new_client_thread = Thread(target=yugioh_server.threaded_client, args=(session_id,))
            new_client_thread.start()
        network.send_data(client_connection, json.dumps({"player": player, "session_id": session_id}).encode('utf-8'))
        


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    initialize_server()
