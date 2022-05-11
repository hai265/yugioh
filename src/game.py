# Game manages the logic of the game, determines the winner of game if one player's health reaches 0,
# manages putting monsters on each player's field.
import random
from enum import IntEnum
from src.player import Player
from src.card import Monster, Spell


class GameStatus(IntEnum):
    """
    Enum for representing the state of the yugioh game
    WAITING: Game has not started yet since another player is needed to connect
    ONGOING: Yugioh game is currently ongoing
    ENDED: Yugioh game has ended
    """
    WAITING = 1
    ONGOING = 2
    ENDED = 3


class GameController:
    """A class that controls the flow and progression of the game.
    """
    def __init__(self, session_id=0):
        self.players = []
        self.current_player = 0
        self.other_player = 1
        self.session_id = session_id
        self.game_status = GameStatus.WAITING

    def determine_first_player(self):
        """Sets starting turn order.
        """
        self.current_player, self.other_player = random.sample([self.current_player, self.other_player], 2)

    def change_turn(self):
        """Changes player turn.
        """
        self.current_player, self.other_player = self.other_player, self.current_player

    def attack_monster(self, attacking_monster: int, attacked_monster: int):
        """Conducts an attack from one of current player's monsters to one of other player's monsters.

        Args:
            attacking_monster: Index on the current player's field of the monster that is attacking. Must be in attack
                position.
            attacked_monster: Index on the other player's field of the monster that is being attacked.
        """
        current = self.get_current_player()
        other = self.get_other_player()
        atk_monster = current.monster_field[attacking_monster]

        if atk_monster.battle_pos == Monster.DEF:
            return

        target_monster = other.monster_field[attacked_monster]

        if target_monster.battle_pos == Monster.ATK:
            atk_difference = atk_monster.attack_points - target_monster.attack_points

            if atk_difference > 0:
                other.decrease_life_points(atk_difference)
                other.send_card_to_graveyard(attacked_monster, -1)
            elif atk_difference == 0:
                current.send_card_to_graveyard(attacking_monster, -1)
                other.send_card_to_graveyard(attacked_monster, -1)
            elif atk_difference < 0:
                current.decrease_life_points(abs(atk_difference))
                current.send_card_to_graveyard(attacking_monster, -1)
        elif target_monster.battle_pos == Monster.DEF:
            atk_difference = atk_monster.attack_points - target_monster.defense_points
            target_monster.face_pos = Monster.FACE_UP

            if atk_difference > 0:
                other.send_card_to_graveyard(attacked_monster, -1)
            elif atk_difference == 0:
                pass
            elif atk_difference < 0:
                current.decrease_life_points(abs(atk_difference))

    def attack_player(self, attacking_monster):
        """Conducts an attack from one of current player's monsters directly towards the other player's life points.

        Args:
            attacking_monster: Index on the current player's field of the monster that is attacking.
        """
        current = self.get_current_player()
        other = self.get_other_player()
        position = current.monster_field[attacking_monster].battle_pos

        if all([monster is None for monster in other.monster_field]) and position == Monster.ATK:
            atk = current.monster_field[attacking_monster].attack_points
            other.decrease_life_points(atk)

    def activate_spell(self, spell_idx: int):
        current = self.get_current_player()
        current.hand[spell_idx].activate_effect()
        current.send_card_to_graveyard(-1, spell_idx)

    def equip_spell(self, target_monster_idx: int, spell_idx: int):
        current = self.get_current_player()
        monster, equip_spell = current.monster_field[target_monster_idx], current.hand[spell_idx]

        if monster.attribute == equip_spell.required_monster_type or \
                monster.monster_type == equip_spell.required_monster_type:
            equip_spell.equipped_monster = monster
            monster.equipped_spell = equip_spell.name

            if current.spell_trap_field[target_monster_idx] is None:
                current.spell_trap_field[target_monster_idx] = equip_spell
            else:
                field_idx = current.spell_trap_field.index(None)
                current.spell_trap_field[field_idx] = equip_spell

            equip_spell.activate_effect()
        else:
            raise ValueError("Specified monster does no meet the requirements for this spell.")

    def is_there_winner(self):
        """Checks if either player has won. A player has won if their opponent's life_points have reached 0.

        Returns:
            True if either player's life point total is 0, False otherwise.
        """
        current = self.get_current_player()
        other = self.get_other_player()

        return current.life_points == 0 or other.life_points == 0

    def get_winner(self):
        """Returns the player that won the game or None if the game was tied.

        Should only be called after is_there_winner returns True.

        Returns:
            Player that won or None if there was a tie
        """
        current = self.get_current_player()
        other = self.get_other_player()

        if self.is_there_winner():
            if current.life_points > 0:
                return current
            elif other.life_points > 0:
                return other
            elif current.life_points == 0 and other.life_points == 0:
                return None

    def normal_summon(self, hand_idx: int):
        """Summons monster from current_players's hand onto current_player's field in face-ip attack positions.

        Args:
            hand_idx: index in current_player's hand of monster to summon
        """
        current = self.get_current_player()
        field_idx = current.monster_field.index(None)
        current.normal_summon(hand_idx, field_idx)

    def normal_set(self, hand_idx: int):
        """Summons monster from current_players's hand onto current_player's field in face-down defense position.

       Args:
           hand_idx: index in current_player's hand of monster to summon
       """
        current = self.get_current_player()
        field_idx = current.monster_field.index(None)
        current.normal_set(hand_idx, field_idx)

    def flip_summon(self, field_idx):
        """Flip a monster in face-down defense position to face-up attack position.

        Args:
            field_idx: Index on the field to place the card.
        """
        current = self.get_current_player()
        current.flip_summon(field_idx)

    def tribute_summon_monster(self, hand_idx: int, tribute1_idx: int, tribute2_idx: int):
        """Tribute summon monster from current player's hand onto current player's field.

        Args:
            hand_idx: index in current_player's hand of monster to summon
            tribute1_idx: index in current_player's field of first tribute monster
            tribute2_idx: index in current_player's field of second tribute monster, only needed when summoning a
                level 7 or higher monster
        """
        current = self.get_current_player()
        current.tribute_summon(hand_idx, tribute1_idx, tribute2_idx)

    def get_current_player(self) -> Player:
        """
        Returns:
            player whose turn it currently is.
        """
        return self.players[self.current_player]

    def get_other_player(self) -> Player:
        """
        Returns:
            Returns the player whose turn it currently is not.
        """
        return self.players[self.other_player]
