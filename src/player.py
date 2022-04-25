from src.card import Monster
from src.card import Card


class Player:
    """Class which represents a player in a Yugioh game.
    """
    FIELD_CARD_LIMIT = 5

    def __init__(self, life_points: int, name: str):
        """Initializes Player with a starting amount of life points and a name.

        Args:
            life_points: Amount of life points the player starts with.
            name: Name of the player.
        """
        self.life_points = life_points
        self.name = name
        self.deck = []
        self.hand = []
        self.graveyard = []
        self.monster_field = [None] * Player.FIELD_CARD_LIMIT  # There are a total of 10 field spots in yugioh
        self.spell_trap_field = [None] * Player.FIELD_CARD_LIMIT

    def draw_card(self, quantity: int) -> None:
        """Draw a specified number cards from the top of the player's deck.

        Args:
            quantity: number of cards to draw
        """
        for _ in range(quantity):
            self.hand.append(self.deck.pop(0))

    def get_hand_size(self) -> int:
        """Getter for the number of cards in player's hand.

        Returns:
            The number of cards in the player's hand.
        """
        return len(self.hand)

    def get_deck_size(self) -> int:
        """Getter for the number of cards in the player's deck.

        Returns:
            The number of cards in the player's deck.
        """
        return len(self.deck)

    def get_graveyard_size(self) -> int:
        """Getter for the number of cards in the player's graveyard.

        Returns:
            The number of cards in the player's graveyard.
        """
        return len(self.graveyard)

    def normal_summon(self, hand_idx: int, field_idx: int, position: str):
        """Removes a monster card from the player's hand and adds it to the field at a specific location.

        Args:
            hand_idx: Index of the card in the player's hand to be summoned.
            field_idx: Index on the field to place the card.
            position: Position to summon monster in.
        Returns:

        """
        monster = self.hand.pop(hand_idx)
        monster.position = position
        self.monster_field[field_idx] = monster

    def tribute_summon(self, hand_idx: int, tribute1_idx: int, tribute2_idx: int, position: str):
        """Removes a monster card from the player's hand and adds it to the field at a specific location.

        Args:
            hand_idx: Index of the card in the player's hand to be summoned.
            tribute1_idx: Index of the first card to tribute.
            tribute2_idx: Index of the second card to tribute, may not be used.
            position: Position to summon monster in.
        """
        monster_to_summon = self.hand[hand_idx]

        if 5 <= monster_to_summon.level < 7 and tribute1_idx >= 0:
            tribute1_valid = self.monster_field[tribute1_idx] is not None

            if tribute1_valid:
                self.send_card_to_graveyard(tribute1_idx, -1)
                field_idx = self.monster_field.index(None)
                self.normal_summon(hand_idx, field_idx, position)
        elif monster_to_summon.level >= 7 and tribute1_idx >= 0 and tribute2_idx >=0:
            tribute1_valid = self.monster_field[tribute1_idx] is not None
            tribute2_valid = tribute2_idx != tribute1_idx and self.monster_field[tribute2_idx] is not None

            if tribute1_valid and tribute2_valid:
                self.send_card_to_graveyard(tribute1_idx, -1)
                self.send_card_to_graveyard(tribute2_idx, -1)
                field_idx = self.monster_field.index(None)
                self.normal_summon(hand_idx, field_idx, position)

    def change_monster_position(self, field_idx: int):
        """Change a monster's battle position.

        Args:
            field_idx: Index of the card on the field whose position will be changed.
        """
        monster = self.monster_field[field_idx]
        monster.position = 'def' if monster.position == 'atk' else 'atk'

    def send_card_to_graveyard(self, field_idx: int, hand_idx: int) -> bool:
        """Get card from either hand or field and send it to the graveyard. A -1 index means that no card from the
            hand/field should be sent to the graveyard
        Params:
            hand_index:int The card in the player's hand to be sent to the graveyard
            field_index:int The location of the card on the field to be sent to the graveyard
        :return `True` if a card was successfully sent to the graveyard, `False` otherwise. A return value of `False`
                means that both parameters had values of -1.
        """

        # Send card on field to graveyard
        if field_idx != -1:
            self.graveyard.append(self.monster_field[field_idx])  # Add card to graveyard
            self.monster_field[field_idx] = None  # Remove the card from the field

        # Send card in player's hand to graveyard
        if hand_idx != -1:
            self.graveyard.append(self.hand[hand_idx])  # Add card to graveyard
            self.hand.pop(hand_idx)  # Remove the card from hand

        return field_idx != -1 or hand_idx != -1

    def decrease_life_points(self, life_points: int):
        """Decrease player's life points by a specified amount.

        Args:
            life_points: The number of points to decrease life points by. If this value is greater than the amount of
                life points the player has, the player's life point total will be set to 0.
        """
        self.life_points -= life_points

        if self.life_points <= 0:
            self.life_points = 0
