# Class for a command line interface to control the yugioh yugioh_game
import json
import os
import pickle
import socket
from asyncio.log import logger
from typing import Union, Any

import inquirer
import websockets
from inquirer import errors

from src.card import monster_card_to_string, spell_card_to_string, Monster, Spell, Card
from src.game import GameController, GameStatus


class NetworkCli:
    """
    Class that represents a yugioh client that connects to a yugioh server, using the command line
    """
    _phase = None

    def __init__(self, server_ip: str, port=5555, name="", deck=[]):
        """
        Name: name of the player
        deck: a list of card names that a player will use for the game
        """
        self.players = []
        self.yugioh_game: GameController = GameController(0)
        self.client_socket = None
        self.session_id = 0
        self.player_place = 0
        self.other_player_place = 1
        self.session_id = 0
        self.name = name
        self.deck = deck
        self.server_ip = server_ip
        self.port = port
        self.num_rounds = 0

    def display_board(self):
        """
        Displays the yugioh_game board and the current player's hand to the command line
        Returns: None
        """
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        print("It is currently " + str(self.yugioh_game.get_current_player().name) + "'s turn" + " Round " + str(
            self.num_rounds))
        for player_place, player in enumerate(self.yugioh_game.players):
            print("{} ({}) 's field:".format(player.name, player.life_points))
            print_str = ""
            for card in player.monster_field:
                if card:
                    if card.face_pos == Monster.FACE_UP:
                        print_str += monster_card_to_string(card) + " | "
                    else:
                        monster_string = " "
                        if player_place == self.player_place:
                            monster_string = monster_card_to_string(card)
                        print_str += monster_string + "(Face down)" + " | "
                else:
                    print_str += "None | "
            print(print_str)

            print_str = ""
            for card in player.spell_trap_field:
                if card:
                    print_str += spell_card_to_string(card) + " | "
                else:
                    print_str += "None | "
            print(print_str)
        print()
        print(
            "Your cards in deck: " + str(
                len(self.yugioh_game.players[self.player_place].deck)))
        print("Your cards in graveyard: " + str(
            len(self.yugioh_game.players[self.player_place].graveyard)))
        print("Your hand ", )
        for card in self.yugioh_game.players[self.player_place].hand:
            if card is None:
                print("None")
            elif isinstance(card, Monster):
                print(monster_card_to_string(card))
            elif isinstance(card, Spell):
                print(spell_card_to_string(card, verbose=True))

    async def start_game(self) -> dict[str, Union[str, Any]]:
        """
        Starts an instance of a yugioh yugioh_game on the command line
        """
        # Initialize players
        self.yugioh_game = GameController()
        print("Waiting for another player...")
        game_state = await self.connect_to_server()
        self.player_place, self.session_id = game_state["player"], game_state["session_id"]
        self.other_player_place = 1 if self.player_place == 0 else 0
        logger.debug("Send Create Game")
        await self.client_socket.send(json.dumps(
            {"operation": "create", "session_id": self.session_id,
             "player_name": self.name,
             "deck": self.deck, "get_pickle": True, "player_place": self.player_place}).encode('utf-8'))

        data = await self.client_socket.recv()
        self.yugioh_game = pickle.loads(data)

        while self.yugioh_game.game_status == GameStatus.WAITING:
            data = await self.client_socket.recv()
            self.yugioh_game = pickle.loads(data)
        await self.send_data_and_update_game(
            {"operation": "update", "player": self.player_place, "session_id": self.session_id,
             "move": "draw_card", "args": [3], "get_pickle": True})
        while GameStatus.ONGOING:
            self.num_rounds += 1
            if self.yugioh_game.current_player != self.player_place:
                self.setState(WaitPhase())
                await self._phase.conduct_phase()
            if self.yugioh_game.game_status == GameStatus.ENDED:
                break
            self.setState(DrawPhase())
            while not isinstance(self._phase, EndPhase):
                if not await self._phase.conduct_phase():
                    game_status = await self.close_game()
                    return game_status
            if self.yugioh_game.is_there_winner():
                break
            await self._phase.conduct_phase()
        game_status = await self.close_game()
        return game_status

    async def connect_to_server(self) -> dict:
        """
        Connects to the game server.
        :return: The game state that the server has
        """
        self.client_socket = await websockets.connect(self.server_ip + ":" + str(self.port), timeout=60,
                                                      close_timeout=60)
        # Keep recieving until get a session_id that is not 0
        while True:
            game_state = json.loads(await self.client_socket.recv())
            if game_state["session_id"] != 0:
                logger.debug("Recieved game start message")
                break
            else:
                logger.debug("Recieved alive message")
        return game_state

    def setState(self, phase: 'Phase'):
        self._phase = phase
        self._phase.context = self

    async def send_data_and_update_game(self, data: dict):
        """
        Method that sends data to the server and recieves data back to update
        Args:
            data: data to send to the server
        """
        try:
            await self.client_socket.send(json.dumps(data).encode("utf-8"))
            self.yugioh_game = pickle.loads(await self.client_socket.recv())
        except socket.error:
            pass

    async def close_game(self):
        """
        Sends a "delete" to the server and closes the client and game
        :return: a dictionary containing key "game_result", corresponds to "w"in, "l"oss, "d"raw
        """
        self.yugioh_game.game_status = GameStatus.ENDED
        if self.yugioh_game.is_there_winner():
            self.yugioh_game.game_status = GameStatus.ENDED
            if self.yugioh_game.players[self.player_place].life_points <= 0 or len(self.yugioh_game.players[self.player_place].deck) <= 0:
                print("You lost")
                game_result = "l"
                await self.send_data_and_update_game(
                    {"operation": "delete", "session_id": self.session_id, "get_pickle": True})
            elif self.yugioh_game.players[self.other_player_place].life_points <= 0 or len(self.yugioh_game.players[self.other_player_place].deck) <=0:
                print("You won!")
                game_result = "w"
                await self.send_data_and_update_game(
                    {"operation": "delete", "session_id": self.session_id, "get_pickle": True})
            else:
                print("Tie")
                game_result = "d"
                await self.send_data_and_update_game(
                    {"operation": "delete", "session_id": self.session_id, "get_pickle": True})
            await self.client_socket.send(json.dumps({"operation": "read", "get_game_actions": True}).encode("utf-8"))

            game_actions = await self.client_socket.recv()
            await self.client_socket.close()
            return {"game_result": game_result, "game_actions": json.loads(game_actions)}

    async def main(self):
        """
        Method to start the main command line interface
        """
        await self.start_game()


class Phase:
    """
    Class that represents the various phases that a yugioh game can be at
    """

    @property
    def context(self) -> NetworkCli:
        return self._context

    @context.setter
    def context(self, context: NetworkCli) -> None:
        self._context = context

    async def conduct_phase(self) -> bool:
        raise NotImplementedError


class DrawPhase(Phase):
    """
    Phase where the player draws a card
    """

    async def conduct_phase(self) -> bool:
        await self.context.send_data_and_update_game(
            {"operation": "update", "player": self._context.player_place, "session_id": self._context.session_id,
             "move": "draw_card", "args": [1], "get_pickle": True})
        if self.context.yugioh_game.get_winner() != False:
            return False
        self.context.display_board()
        self.context.setState(MainPhase())
        return True


class MainPhase(Phase):
    """
    Phase in which the player can summon cards, change battle positions of monsters, play spells
    """

    async def conduct_phase(self) -> bool:
        while True:
            self.context.display_board()
            questions = [
                inquirer.List('choice',
                              message="Choose your action",
                              choices=['Summon a monster', 'Activate Spell', 'Go to Battle Phase'],
                              ),
            ]
            answers = inquirer.prompt(questions)
            if answers['choice'] == "Go to Battle Phase":
                break
            if answers['choice'] == 'Summon a monster':
                questions = [
                    inquirer.List('choice',
                                  message="Choose a summoning method summon",
                                  choices=["Normal Summon", "Tribute Summon", "Flip Summon", "Cancel"],
                                  ),
                ]
                what_summon = inquirer.prompt(questions)["choice"]
                if what_summon == "Cancel":
                    continue
                if what_summon == "Normal Summon":
                    hand_choices = generate_card_question(
                        self.context.yugioh_game.get_current_player().hand)
                    hand_choices.append(("Cancel", -1))
                    questions = [
                        inquirer.List('choice', message="Choose a monster from your hand to summon",
                                      choices=hand_choices, ), ]
                    choice = inquirer.prompt(questions)["choice"]
                    if choice == -1:
                        continue
                    await self.normal_summon(choice)
                elif what_summon == "Tribute Summon":
                    hand_choices = generate_card_question(
                        self.context.yugioh_game.get_current_player().hand)
                    hand_choices.append(("Cancel", -1))
                    questions = [inquirer.List('choice', message="Choose a monster from your hand to summon",
                                               choices=hand_choices, ), ]
                    await self.tribute_summon(inquirer.prompt(questions)["choice"])
                elif what_summon == "Flip Summon":
                    await self.flip_summon()
                else:
                    break
            elif answers['choice'] == "Activate Spell":
                hand_choices = generate_spell_card_question(self.context.yugioh_game.get_current_player().hand)
                hand_choices.append(("Cancel", -1))
                questions = [
                    inquirer.List('choice',
                                    message="Choose a spell from your hand to use",
                                    choices=hand_choices,
                                    ),
                ]

                spell_to_use = inquirer.prompt(questions)["choice"]
                if spell_to_use == -1:
                    continue
                await self.activate_spell(spell_to_use)
                self.context.display_board()
        self.context.display_board()
        self.context.setState(BattlePhase())
        return True

    async def normal_summon(self, monster_to_summon: int):
        """
        Method that handles getting input to normal summon a monster from a person's hand
        :param monster_to_summon: The index of a monster in a player's hand
        """
        questions = [
            inquirer.List('choice',
                          message="Choose a position to summon",
                          choices=["Face Up", "Face Down", "Cancel"],
                          ),
        ]
        position = inquirer.prompt(questions)["choice"]
        if position == "Cancel":
            return
        if position == "Face Up":
            await self.context.send_data_and_update_game(
                {"operation": "update", "session_id": self.context.session_id,
                 "move": "normal_summon", "args":
                     [monster_to_summon], "get_pickle": True})
        elif position == "Face Down":
            await self.context.send_data_and_update_game(
                {"operation": "update", "session_id": self.context.session_id,
                 "move": "normal_set", "args":
                     [monster_to_summon], "get_pickle": True})
            self.context.display_board()

    async def tribute_summon(self, monster_to_summon):
        """
        Method that handles getting input to tribute summon a monster from a person's hand
        :param monster_to_summon: The index of a monster in a player's hand
                """
        if monster_to_summon == -1:
            return

        def validator(_, answers):
            if -1 in answers or len(answers) == 2:
                return True
            else:
                raise errors.ValidationError('', reason='You must select two monsters on the field to proceed.')

        monster_choices = generate_card_question(self.context.yugioh_game.get_current_player().monster_field)
        monster_choices.append(("Cancel", -1))
        questions = [
            inquirer.Checkbox('choice',
                              message="Choose two monsters to sacrifice on your field. (Press space to select and "
                                      "enter to finalize)",
                              choices=monster_choices, validate=validator
                              ),
        ]
        monsters_to_sacrifice = inquirer.prompt(questions)["choice"]
        if len(monsters_to_sacrifice) == 0 or -1 in monsters_to_sacrifice:
            return
        await self.context.send_data_and_update_game(
            {"operation": "update", "session_id": self.context.session_id,
             "move": "tribute_summon", "args":
                 [monster_to_summon, monsters_to_sacrifice[0], monsters_to_sacrifice[1]], "get_pickle": True})
        self.context.display_board()

    async def activate_spell(self, spell):
        """Method that handles input to use a spell card.

        Args:
            spell: Index of spell card to use.
        """
        if spell == -1:
            return

        questions = [
            inquirer.List('choice',
                          message="Decide whether or not to activate the spell",
                          choices=["Activate", "Cancel"],
                          ),
        ]

        decision = inquirer.prompt(questions)["choice"]
        if decision == "Cancel":
            return

        spell_icon = self.context.yugioh_game.get_current_player().hand[spell].icon
        if spell_icon == Spell.Icon.NORMAL:
            await self.context.send_data_and_update_game(
                {"operation": "update", "session_id": self.context.session_id, "move": "normal_spell",
                 "args": [spell], "get_pickle": True}
            )
        elif spell_icon == Spell.Icon.EQUIP:
            required_type = get_required_type(self.context.yugioh_game.get_current_player().hand[spell].name)
            monster_choices = generate_equip_spell_card_question(
                self.context.yugioh_game.get_current_player().monster_field, required_type)
            monster_choices.append(("Cancel", -1))

            questions = [
                inquirer.List('choice',
                              message="(Press space to select and enter to finalize)",
                              choices=monster_choices
                              ),
            ]

            monster = inquirer.prompt(questions)["choice"]
            if monster == "Cancel":
                return

            await self.context.send_data_and_update_game(
                {"operation": "update", "session_id": self.context.session_id, "move": "equip_spell",
                 "args": [monster, spell], "get_pickle": True}
            )
        self.context.display_board()
        
    async def flip_summon(self):
        """
        Method that handles getting input to flip summon a face down monster from a player's field
        """
        choices = generate_card_question(
            self.context.yugioh_game.get_current_player().monster_field,
            card_filter=lambda monster: isinstance(monster, Monster) and monster.face_pos == Monster.FACE_DOWN)
        choices.append(("Cancel", -1))
        questions = [inquirer.List('choice', message="Choose monster to flip summon", choices=choices, ), ]
        card_to_flip = inquirer.prompt(questions)["choice"]
        if card_to_flip == -1:
            return
        await self.context.send_data_and_update_game(
            {"operation": "update", "session_id": self.context.session_id,
             "move": "flip_summon", "args":
                 [card_to_flip], "get_pickle": True})
        self.context.display_board()


class BattlePhase(Phase):
    """
    Phase where the player can attack monsters and the player
    """

    async def conduct_phase(self) -> bool:
        while True:
            self.context.display_board()
            monster_choices = generate_card_question(
                self.context.yugioh_game.get_current_player().monster_field,
                card_filter=lambda card: isinstance(card, Monster) and card.can_attack)
            monster_choices.append(("End Phase", -1))

            questions = [
                inquirer.List('choice',
                              message="Choose a monster on your field",
                              choices=monster_choices),
            ]
            attacking_monster = inquirer.prompt(questions)["choice"]
            if attacking_monster == -1:
                break
            target = []
            if not self.context.yugioh_game.get_other_player().can_be_attacked():
                target = generate_card_question(
                    self.context.yugioh_game.get_other_player().monster_field,
                    card_filter=lambda monster: isinstance(monster, Monster) and monster.face_pos == Monster.FACE_UP)
            else:
                target.append(("Attack Player", 5))
            target.append(("Cancel", -1))
            questions = [
                inquirer.List('choice',
                              message="Choose a target",
                              choices=target),
            ]
            targeted_monster = inquirer.prompt(questions)["choice"]
            if targeted_monster == -1:
                continue
            else:
                if targeted_monster == 5:
                    await self.context.send_data_and_update_game(
                        {"operation": "update", "session_id": self.context.session_id,
                         "move": "attack_player", "args": [attacking_monster],
                         "get_pickle": True})
                else:
                    await self.context.send_data_and_update_game(
                        {"operation": "update", "move": "attack_monster", "args":
                            [attacking_monster, targeted_monster],
                         "get_pickle": True})
            self.context.display_board()
            if self.context.yugioh_game.is_there_winner():
                return False
        self.context.setState(EndPhase())
        return True


class EndPhase(Phase):
    """
    Phase where the player ends their turn
    """

    async def conduct_phase(self) -> bool:
        await self.context.send_data_and_update_game(
            {"operation": "update", "session_id": self.context.session_id, "move": "change_turn",
             "args": [], "get_pickle": True})
        self.context.display_board()
        self.context.setState(WaitPhase())
        return True


class WaitPhase(Phase):
    """
    Phase where the player waits while the other player plays
    :returns True if the game can proceed. False if the game ended
    """

    async def conduct_phase(self) -> bool:
        while self.context.yugioh_game.current_player != self.context.player_place:
            self.context.display_board()
            print("It is not your turn yet")
            data = await self.context.client_socket.recv()
            self.context.yugioh_game = pickle.loads(data)
            if self.context.yugioh_game.game_status == GameStatus.ENDED:
                return False
        self.context.num_rounds += 1
        self.context.setState(DrawPhase())
        return True


class Context:
    """
    Context that is used to access the current yugioh game state
    """
    _state = None

    def __init__(self, state: Phase) -> None:
        self.setState(state)

    def setState(self, state: Phase):
        print(f"Context: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self


def generate_card_question(card_choices: list[Card],
                           card_filter=lambda card: isinstance(card, Monster)) -> list[tuple[str, int]]:
    """
    Generate a list of card questions for an inquiry
    :param card_choices: A list of cards
    :param card_filter: a method to filter the cards by
    :return: a
    """
    monster_choices = []
    for field_idx, card in enumerate(card_choices):
        if card_filter(card):
            monster_choices.append((card.name, field_idx))
    return monster_choices


def generate_spell_card_question(card_choices: list) -> list[tuple[str, int]]:
    """Generate a list of spell card questions for an inquiry

    Args:
        card_choices: A list of cards

    Returns:
        List of valid spell choices
    """
    return [(card.name, field_idx) for field_idx, card in enumerate(card_choices) if card and isinstance(card, Spell)]


def generate_equip_spell_card_question(card_choices: list, required_type: str) -> list[tuple[str, int]]:
    """Generate a list of spell card questions for an inquiry

    Args:
        card_choices: A list of cards

    Returns:
        List of valid spell choices
    """
    monster_choices = []
    for field_idx, card in enumerate(card_choices):
        if card and isinstance(card, Monster) and (card.attribute == required_type or
                                                   card.monster_type == required_type):
            monster_choices.append((card.name, field_idx))
    return monster_choices


def get_required_type(spell_name):
    if spell_name == "Book of Secret Arts":
        return "Spellcaster"
    elif spell_name == "Sword of Dark Destruction":
        return "Dark"
    elif spell_name == "Dark Energy":
        return "Fiend"
    elif spell_name == "Invigoration":
        return "Earth"

