from operator import attrgetter
from src.player import Player
from src.card import Monster, Spell
from typing import Union


class Effect:
    """This class implements the different effects used in the implementation of spell cards.
    """

    def __init__(self, player: Player, opponent: Player):
        """Initializes the Effect class with references to the current player and opponent.

        Args:
            player: Object that can activate effects.
            opponent: Object that can be effected by effect activations.
        """
        self.player = player
        self.opponent = opponent

    def increase_life_points(self, life_points: int):
        """Increases the player's life points by a specified amount.

        Args:
            life_points: Amount increase the player's life points by.
        """
        self.player.life_points += life_points

    def decrease_opponent_life_points(self, life_points: int):
        """Decreases the opponent's life points by a specified amount.

        Args:
            life_points: Amount to decrease the opponent's life points by.
        """
        self.opponent.life_points -= life_points

        if self.opponent.life_points < 0:
            self.opponent.life_points = 0

    def destroy_all_monsters(self):
        """Destroys all monsters on the field and sends them to the respective player's graveyard.
        """
        for field_idx in range(Player.FIELD_CARD_LIMIT):
            if self.player.monster_field[field_idx]:
                self.player.send_card_to_graveyard(field_idx, -1)

            if self.opponent.monster_field[field_idx]:
                self.opponent.send_card_to_graveyard(field_idx, -1)

    def destroy_opponent_monster_with_lowest_atk(self):
        """Destroy the opponent's monster with the lowest attack points.
        """
        min_atk_monsters = [min([monster for monster in self.opponent.monster_field if monster],
                            key=attrgetter('attack_points'))]
        min_atk_idx = self.opponent.monster_field.index(min_atk_monsters[0])
        self.opponent.send_card_to_graveyard(min_atk_idx, -1)

    def alter_monster_stats(self, monster: Monster, attack_points: int, defense_points: int):
        """Buffs and/or de-buffs a specified monster's attack and defense by specified values.

        Args:
            monster: Monster to apply the buff/de-buff too.
            attack_points: Amount to increase the monster's attack points by.
            defense_points: Amount to increase the monster's defense points by.
        """
        monster.attack_points += attack_points
        monster.defense_points += defense_points

    def peek_into_opponent_deck(self, num_cards: int) -> list:
        """Allows the player to look at a specified number of cards from the top of the opponent's deck.

        Args:
            num_cards: Number of cards to look at.

        Returns:
            A list containing the cards from the opponents deck
        """
        return self.opponent.deck[:num_cards]

    def peek_into_opponent_hand(self, card_idx: int) -> Union[Monster, Spell]:
        """Allows the player to look at a specified number of cards from the top of the opponent's deck.

       Args:
           card_idx: Index of the card from the opponent's hand.

       Returns:
           The card that was chosen from the opponents hand.
       """
        return self.opponent.hand[card_idx]
