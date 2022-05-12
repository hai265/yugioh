from operator import attrgetter
from src.player import Player

from typing import Union


def increase_life_points(player: Player, opponent: Player, life_points: int):
    """Increases the player's life points by a specified amount.

    Args:
        player:
        opponent:
        life_points: Amount increase the player's life points by.
    """
    player.life_points += life_points


def decrease_opponent_life_points(player: Player, opponent: Player, life_points: int):
    """Decreases the opponent's life points by a specified amount.

    Args:
        life_points: Amount to decrease the opponent's life points by.
    """
    opponent.decrease_life_points(life_points)


def destroy_all_monsters(player: Player, opponent: Player):
    """Destroys all monsters on the field and sends them to the respective player's graveyard.
    """
    for field_idx in range(Player.FIELD_CARD_LIMIT):
        if player.monster_field[field_idx]:
            player.send_card_to_graveyard(field_idx, -1)

        if opponent.monster_field[field_idx]:
            opponent.send_card_to_graveyard(field_idx, -1)


def destroy_opponent_monster_with_lowest_atk(player: Player, opponent: Player):
    """Destroy the opponent's monster with the lowest attack points.
    """
    min_atk_monsters = [min([monster for monster in opponent.monster_field if monster],
                            key=attrgetter('attack_points'))]
    min_atk_idx = opponent.monster_field.index(min_atk_monsters[0])
    opponent.send_card_to_graveyard(min_atk_idx, -1)


def alter_monster_stats(monster, attack_points: int, defense_points: int):
    """Buffs and/or de-buffs a specified monster's attack and defense by specified values.

    Args:
        monster: Monster to apply the buff/de-buff too.
        attack_points: Amount to increase the monster's attack points by.
        defense_points: Amount to increase the monster's defense points by.
    """
    monster.attack_points += attack_points
    monster.defense_points += defense_points


# class Effect:
#     """This class implements the different effects used in the implementation of spell cards.
#     """
#
#     def __init__(self, player: Player, opponent: Player):
#         """Initializes the Effect class with references to the current player and opponent.
#
#         Args:
#             player: Object that can activate effects.
#             opponent: Object that can be effected by effect activations.
#         """
#
#     def increase_life_points(self, player, opponent, life_points: int):
#         """Increases the player's life points by a specified amount.
#
#         Args:
#             life_points: Amount increase the player's life points by.
#         """
#         player.life_points += life_points
#
#     def decrease_opponent_life_points(self, player: Player, opponent: Player, life_points: int):
#         """Decreases the opponent's life points by a specified amount.
#
#         Args:
#             life_points: Amount to decrease the opponent's life points by.
#         """
#         opponent.decrease_life_points(life_points)
#
#     def destroy_all_monsters(self, player, opponent):
#         """Destroys all monsters on the field and sends them to the respective player's graveyard.
#         """
#         for field_idx in range(Player.FIELD_CARD_LIMIT):
#             if self.player.monster_field[field_idx]:
#                 self.player.send_card_to_graveyard(field_idx, -1)
#
#             if self.opponent.monster_field[field_idx]:
#                 self.opponent.send_card_to_graveyard(field_idx, -1)
#
#     def destroy_opponent_monster_with_lowest_atk(self,  player, opponent):
#         """Destroy the opponent's monster with the lowest attack points.
#         """
#         min_atk_monsters = [min([monster for monster in self.opponent.monster_field if monster],
#                             key=attrgetter('attack_points'))]
#         min_atk_idx = self.opponent.monster_field.index(min_atk_monsters[0])
#         self.opponent.send_card_to_graveyard(min_atk_idx, -1)
#
#     def alter_monster_stats(self, monster: Monster, attack_points: int, defense_points: int):
#         """Buffs and/or de-buffs a specified monster's attack and defense by specified values.
#
#         Args:
#             monster: Monster to apply the buff/de-buff too.
#             attack_points: Amount to increase the monster's attack points by.
#             defense_points: Amount to increase the monster's defense points by.
#         """
#         monster.attack_points += attack_points
#         monster.defense_points += defense_points
