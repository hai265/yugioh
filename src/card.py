class Card:
    """
        A class representing a Yu-Gi-Oh! Card.
    """
    def __init__(self, name: str, description: str, card_type: str):
        """
        Initializes the generic fields of a Yu-Gi-Oh! Card.
        :param name: A string containing the name of the card.
        :param description: A string containing a Yu-Gi-Oh! card description.
        :param card_type: A string containing the card's type (Monster, Spell, Trap)
        """
        self.name = name
        self.description = description
        self.card_type = card_type

    def display_card(self) -> dict:
        """
            Gets the information for the current card.
        :return:
            display_info:
                Dictionary containing the instance variables of the Card class.
        """
        return {"name": self.name, "card_type": self.card_type, "description": self.description}


class Monster(Card):
    """
        A class representing a Yu-Gi-Oh! Monster Card.

        Note: This class only supports Normal monsters in the current build.
    """
    def __init__(self, name: str, description: str, attribute: str, monster_type: str,
                 level: int, attack_points: int, defense_points: int):
        """
        Initializes the Monster class with the specified parameters
        :param name: A string containing the name of the monster card.
        :param description: A string containing a Yu-Gi-Oh! card description.
        :param attribute: A string containing the attribute of the monster (DARK LIGHT WATER FIRE EARTH WIND DIVINE)
        :param monster_type: A string containing the monster's type (Warrior, Beast-Warrior, Spellcaster, Fiend, etc.)
        :param level: An integer defining the level of the monster. (Ranges from 1 to 12)
        :param attack_points: An integer defining the monster's attack points.
        :param defense_points: An integer defining the monster's defense points.
        """
        super().__init__(name, description, "Monster")
        self.attribute = attribute
        self.attack_points = attack_points
        self.defense_points = defense_points
        self.level = level
        self.monster_type = monster_type

    def display_card(self) -> dict:
        """
            Gets the information for the current monster card.
        :return:
            display_info:
                a dict containing the instance variables for the monster card.
        """
        display_info = super().display_card()
        display_info["level"] = self.level
        display_info["attribute"] = self.attribute
        display_info["monster_type"] = self.monster_type
        display_info["ATK"] = self.attack_points
        display_info["DEF"] = self.defense_points
        return display_info
