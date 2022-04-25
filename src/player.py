class Player:
    default_life_points = 8000

    def __init__(self, lifepoints: int, name: str):
        """
        Class to represent a player in a yugioh game
        :param lifepoints: amount of lifepoints that the player has
        :param name: name of the player
        """
        self.life_points = lifepoints
        self.name = name
        self.deck = []
        self.hand = []
        self.graveyard = []
        self.field = [None] * 5  # There are a total of 10 field spots in yugioh

    def draw_card(self):
        """Draw a card from the top of the player's deck and add it to the player's hand"""
        # Pop top card of deck list
        card = self.deck.pop(0)

        # Append new card to hand list
        self.hand.append(card)

    def get_hand_size(self) -> int:
        """ Getter for the number of cards in hand

        Returns:
            int: number of cards in player's hand
        """
        return len(self.hand)

    def get_deck_size(self) -> int:
        """ Getter for the number of cards in the player's deck

        Returns:
            int: number of cards in the player's deck
        """
        return len(self.deck)

    def get_graveyard_size(self) -> int:
        """ Getter for the number of cards in the player's graveyard

        Returns:
            int: number of cards in the player's graveyard
        """
        return len(self.graveyard)

    def summon_monster(self, hand_index: int, field_index: int):
        """ Removes a card from the player's hand and adds it to the field at a specific location
        Params:
            hand_index:int The card in the player's hand to be summoned
            field_index:int The location on the field to place the card
        """
        # self.field[field_index] = self.hand.pop(hand_index)

        # Store card from player's hand
        card = self.hand.pop(hand_index)

        # Put the card on the field
        self.field[field_index] = card

    def tribute_summon(self, hand_index: int, field_index: int):
        """ Removes a card from the player's hand and adds it to the field at a specific location

        DEV NOTE: We will wait to implement this after determining the best logic to execute a tribute summon
        Params:
            hand_index:int The card in the player's hand to be summoned
            field_index:int The location on the field to place the card
        """
        pass

    def send_card_to_graveyard(self, field_index: int, hand_index: int):
        """Get card from either hand or field and send it to the graveyard. A -1 index means that no card from the
            hand/field should be sent to the graveyard
        Params:
            hand_index:int The card in the player's hand to be sent to the graveyard
            field_index:int The location of the card on the field to be sent to the graveyard
        """

        # Send card on field to graveyard
        if field_index != -1:
            self.graveyard.append(self.field[field_index])  # Add card to graveyard
            self.field[field_index] = None  # Remove the card from the field

        # Send card in player's hand to graveyard
        if hand_index != -1:
            self.graveyard.append(self.hand[hand_index])  # Add card to graveyard
            self.hand.pop(hand_index)  # Remove the card from hand

    def decrease_life_points(self, life_points: int):
        """Decrease player's life points by a certain amount

        Params:
            life_points:int The number of points to decrease life points by
        """
        self.life_points -= life_points
