import asyncio
from pprint import pprint

import inquirer
from src import database_functions

from src.account_menu import display_prompt
from src.card import deck_to_card_name_list, create_deck_from_preset
from src.client import NetworkCli
from src.database_functions import update_win_loss_draw
import os


def clear_screen():
    """
    Clears the command line screen
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def display_stats(name: str, stats: dict):
    """
    Displays a user's stats
    Args:
    :name: A user's name
    :stats: a dictionary containing "wins", "losses", "draws"
    """
    if "error" in stats:
        print(stats["error"])
        return
    print(f'{name}\'s stats:')
    print(f'Wins {stats["wins"]}')
    print(f'Losses {stats["losses"]}')
    print(f'Draws {stats["draws"]}')


class GameMenu:
    """
    Game menu that starts when a user launches the game
    args:
    server_ip: Server ip of the game server. must be in format ws://server_ip_here
    server_port: port that the server listens on
    """

    def __init__(self, server_ip, server_port):
        self.name = None
        self.user_info = None
        self.name: str
        self.deck_list: list[dict[str: list[str]]]
        self.server_ip = server_ip
        self.server_port = server_port
        self.game_actions = []

    def main(self):
        """
        Main function
        """
        self.authenticate_user()
        while True:
            questions = [
                inquirer.List('choice',
                              message="Menu: (Use arrow keys to select, press enter to choose)",
                              choices=['Play a game', 'Create and view decks', 'Stats', "View last game", "Exit Game"],
                              ),
            ]
            answers = inquirer.prompt(questions)
            if answers['choice'] == "Play a game":
                asyncio.run(self.play_game())
            elif answers['choice'] == "Create and view decks":
                pass
            elif answers['choice'] == "Exit Game":
                print("Have a nice day!")
                return
            elif answers['choice'] == "Stats":
                self.leaderboard()
            elif answers['choice'] == "View last game":
                self.view_last_game()

    def authenticate_user(self):
        """
        Prompts the user to log in or register
        :return:
        """
        self.user_info = display_prompt()
        self.name = self.user_info["name"]
        print("Welcome " + self.name)

    async def play_game(self):
        """
        Runs the yugioh command line game and updates stats according to the game result
        """
        # Use preset decks for now
        preset_deck = create_deck_from_preset("sources/preset1")
        preset_deck = deck_to_card_name_list(preset_deck)
        cli = NetworkCli(self.server_ip, self.server_port, self.name, preset_deck)
        game_result = await cli.start_game()
        self.game_actions = game_result["game_actions"]
        if game_result["game_result"] == "l":
            update_win_loss_draw(self.name, "l")
        elif game_result["game_result"] == "w":
            update_win_loss_draw(self.name, "w")
        elif game_result["game_result"] == "d":
            update_win_loss_draw(self.name, "d")
        else:
            print("Could not update game")
        return

    def leaderboard(self):
        """
        Users can view their own stats as well as other player's stats
        """
        clear_screen()
        display_stats(self.name, database_functions.get_user_stats(self.name))
        while True:
            questions = [
                inquirer.List('choice', message="Choose your action", choices=["Look up player stats", "Exit"],)]
            answer = inquirer.prompt(questions)
            if answer['choice'] == "Look up player stats":
                lookup_name = inquirer.prompt([inquirer.Text("name", message="Enter a name")])["name"]
                display_stats(lookup_name,  database_functions.get_user_stats(lookup_name))
            else:
                return

    def view_last_game(self):
        """
        A way for a user to view the actions taken by both players during their last match
        """
        if self.game_actions:
            for log_message in self.game_actions:
                print(f" Turn {log_message['turn']}: {log_message['message']}")
        else:
            print("You did not play a game yet.")