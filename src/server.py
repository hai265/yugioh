# !/usr/bin/env python

# Code adapted from https://websockets.readthedocs.io/en/stable/intro/tutorial2.html
import asyncio
import json
import logging
import socket
from collections import defaultdict

import websockets

from src.yugioh import Yugioh

JOIN = {}

WATCH = {}


class YugiohServer:
    def __init__(self, server_ip: str, port: int):
        self.games: dict[int, Yugioh] = {}
        self.id_count = 0
        self.id_to_sockets: dict[int, list[socket.socket]] = defaultdict(
            list)  # Dict that maps session_id to sockets associated with the game
        self.server_ip = server_ip
        self.port = port

    async def error(self, websocket, message):
        """
        Send an error message.
        """
        event = {
            "type": "error",
            "message": message,
        }
        await websocket.send(json.dumps(event))

    # TODO: Put the processing crud part here
    async def play(self, websocket, session_id: int):
        """
        Receive and process moves from a player.
        """
        async for data in websocket:
            # Parse a "play" event from the UI.
            logging.info("Recieved data from " + str(websocket))
            data = json.loads(data)
            send_data = None
            if session_id in self.games:
                game = self.games[session_id]
                broadcast_sockets = self.id_to_sockets[session_id]
                if data["operation"] == "create":
                    send_data = game.create_game(data)
                elif data["operation"] == "read":
                    send_data = game.read_game(data)
                    broadcast_sockets = [websocket]
                elif data["operation"] == "update":
                    send_data = game.update_game(data)
                elif data["operation"] == "delete":
                    send_data = game.delete_game(data)
                else:
                    logging.warning("Invalid operation")
                # Don't broadcast to both players if was a read_game
                if data.get("get_pickle", False):
                    websockets.broadcast(broadcast_sockets, send_data)
                else:
                    websockets.broadcast(broadcast_sockets, json.dumps(send_data).encode("utf-8"))

    # TODO: Put the initializing game and join part here
    async def create_new_game(self, websocket):
        """
        Handle a connection from the first player: start a new game.
        """
        # Initialize a Connect Four game, the set of WebSocket connections
        # receiving moves from this game, and secret access tokens.
        session_id = ((self.id_count - 1) // 2) + 1
        self.games[session_id] = Yugioh()
        try:
            await self.play(websocket, session_id)
        finally:
            self.id_count -= 1
            self.id_to_sockets[session_id].remove(websocket)

    # TODO: Put the join existing code here
    async def join_existing_game(self, websocket, session_id: int):
        """
        Handle a connection from the second player: join an existing game.
        """
        try:
            self.games[session_id]
        except KeyError:
            await self.error(websocket, "Game not found.")
            return
        try:
            for player_place, websocket in enumerate(self.id_to_sockets[session_id]):
                event = {
                    "session_id": session_id,
                    "player": player_place,
                }
                await websocket.send(json.dumps(event))
            await self.play(websocket, session_id)
        finally:
            self.id_count -= 1
            self.id_to_sockets[session_id].remove(websocket)

    # TODO: Put the connecting sockets part here
    async def handler(self, websocket):
        """
        Handle a connection and dispatch it according to who is connecting.

        """
        # Receive and parse the "init" event from the UI.
        try:
            logging.info(f'Connected to: {websocket}')
            self.id_count += 1
            logging.info("Id count: " + str(self.id_count))
            session_id = ((self.id_count - 1) // 2) + 1
            self.id_to_sockets[session_id].append(websocket)
            if self.id_count % 2 == 1:
                await self.create_new_game(websocket)
            else:
                # Second player joins an existing game.
                await self.join_existing_game(websocket, session_id)
        finally:
            return

    async def main(self):
        async with websockets.serve(self.handler, self.server_ip, self.port, ping_timeout=160):
            await asyncio.Future()  # run forever


def initialize_server():
    server = YugiohServer("0.0.0.0", 5555)
    logging.getLogger().setLevel(logging.INFO)
    asyncio.run(server.main())
# if __name__ == "__main__":
#     asyncio.run(main())
