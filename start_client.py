import asyncio
import logging

from src.game_menu import GameMenu


def main():
    SERVER_IP = "ws://167.172.152.60"
    #SERVER_IP = "ws://localhost"
    SERVER_PORT = 5555
    logging.getLogger().setLevel(logging.INFO)
    game_menu = GameMenu(SERVER_IP, SERVER_PORT)
    game_menu.main()


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
