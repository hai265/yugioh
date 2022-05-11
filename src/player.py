from src.card import Monster


class Player:
    """Class which represents a player in a Yugioh game.
    """
    FIELD_CARD_LIMIT = 5
    DEFAULT_LIFE_POINTS = 8000

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

    def draw_card(self, quantity=1) -> None:
        """Draw a specified number cards from the top of the player's deck.

        Args:
            quantity: number of cards to draw. If not specified, defaults to 1
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

    def normal_summon(self, hand_idx: int, field_idx: int):
        """Removes a monster card from the player's hand and adds it to the field at a specific location.

        Normal summon always summons the monster in face-up attack position.

        Args:
            hand_idx: Index of the card in the player's hand to be summoned.
            field_idx: Index on the field to place the card.
        """
        self.monster_field[field_idx] = self.hand.pop(hand_idx)

    def normal_set(self, hand_idx: int, field_idx: int):
        """Removes a monster card from the player's hand and adds it to the field at a specific location.

        Normal set always summons the monster in face-down defense position.

        Args:
            hand_idx: Index of the card in the player's hand to be set.
            field_idx: Index on the field to place the card.
        """
        monster = self.hand.pop(hand_idx)
        monster.face_pos = Monster.FACE_DOWN
        monster.battle_pos = Monster.DEF
        self.monster_field[field_idx] = monster

    def flip_summon(self, field_idx: int):
        """Flip a monster in face-down defense position to face-up attack position.

        Args:
            field_idx: Index on the field to place the card.
        """
        monster = self.monster_field[field_idx]
        monster.face_pos = Monster.FACE_UP
        monster.battle_pos = Monster.ATK

    def tribute_summon(self, hand_idx: int, tribute1_idx: int, tribute2_idx: int):
        """Removes a monster card from the player's hand and adds it to the field at a specific location.

        Tribute summon always summons the monster in face-up attack position.

        Args:
            hand_idx: Index of the card in the player's hand to be summoned.
            tribute1_idx: Index of the first card to tribute.
            tribute2_idx: Index of the second card to tribute, may not be used.
        """
        monster_to_summon = self.hand[hand_idx]

        if 5 <= monster_to_summon.level < 7 and tribute1_idx >= 0:
            tribute1_valid = self.monster_field[tribute1_idx] is not None

            if tribute1_valid:
                self.send_card_to_graveyard(tribute1_idx, -1)
                field_idx = self.monster_field.index(None)
                self.normal_summon(hand_idx, field_idx)
        elif monster_to_summon.level >= 7 and tribute1_idx >= 0 and tribute2_idx >= 0:
            tribute1_valid = self.monster_field[tribute1_idx] is not None
            tribute2_valid = tribute2_idx != tribute1_idx and self.monster_field[tribute2_idx] is not None

            if tribute1_valid and tribute2_valid:
                self.send_card_to_graveyard(tribute1_idx, -1)
                self.send_card_to_graveyard(tribute2_idx, -1)
                field_idx = self.monster_field.index(None)
                self.normal_summon(hand_idx, field_idx)

    def change_monster_battle_position(self, field_idx: int):
        """Change a monster's battle position.

        Args:
            field_idx: Index of the card on the field whose position will be changed.
        """
        monster = self.monster_field[field_idx]
        monster.battle_pos = Monster.DEF if monster.battle_pos == Monster.ATK else Monster.ATK

    def send_card_to_graveyard(self, monster_field_idx: int, hand_idx: int, spell_field_idx=-1) -> bool:
        """Get card from either hand or field and send it to the graveyard. A -1 index means that no card from the
        hand/field should be sent to the graveyard

        Args:
            hand_idx:int The card in the player's hand to be sent to the graveyard.
            monster_field_idx: int The location of the card on the monster field to be sent to the graveyard.
            spell_field_idx: The location of the card on the spell field to be sent to the graveyard.

        Returns: `True` if a card was successfully sent to the graveyard, `False` otherwise. A return value of `False`
                means that both parameters had values of -1.
        """

        # Send card on field to graveyard
        if monster_field_idx != -1:
            monster = self.monster_field[monster_field_idx]
            monster.reset_stats()
            spell_name = monster.equipped_spell

            self.graveyard.append(self.monster_field[monster_field_idx])  # Add monster to graveyard
            self.monster_field[monster_field_idx] = None  # Remove the monster from the field

            if spell_name:
                spell_idx = [i for i, spell in enumerate(self.spell_trap_field) if spell and spell.equipped_monster
                             is monster][0]
                # spell_idx = self.spell_trap_field.index(spell)
                self.graveyard.append(self.spell_trap_field[spell_idx])  # Add spell to graveyard
                self.spell_trap_field[spell_idx] = None  # Remove the spell from the field

        if spell_field_idx != -1:
            spell = self.spell_trap_field[spell_field_idx]
            monster = spell.equipped_monster

            if monster:
                monster.reset_stats()

            self.graveyard.append(self.spell_trap_field[spell_field_idx])  # Add spell to graveyard
            self.spell_trap_field[spell_field_idx] = None  # Remove the spell from the field

        # Send card in player's hand to graveyard
        if hand_idx != -1:
            self.graveyard.append(self.hand[hand_idx])  # Add card to graveyard
            self.hand.pop(hand_idx)  # Remove the card from hand

        return monster_field_idx != -1 or hand_idx != -1

    def decrease_life_points(self, life_points: int):
        """Decrease player's life points by a specified amount.

        Args:
            life_points: The number of points to decrease life points by. If this value is greater than the amount of
                life points the player has, the player's life point total will be set to 0.
        """
        self.life_points -= life_points

        if self.life_points <= 0:
            self.life_points = 0
