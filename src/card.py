import csv


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


def create_card(card_name: str):
    """
        Args: card_name: The name of the card to be created
        Returns: a Card type corresponding to the card name, or None if no card exists with that name
    """
    with open('sources/cards.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0].lower().replace(" ", "") == card_name.lower().replace(" ", ""):
                return Monster(name=row[0], attribute=row[2], monster_type=row[3], level=int(row[4]),
                               attack_points=int(row[5]),
                               defense_points=int(row[6]), description=row[7])
        return None


def create_deck_from_array(card_name_array: list):
    """Method that creates a deck given an array of strings of card names
        Args:
            card_name_array: an array of strings of card names to build the deck
        Returns:
            a list containing Card objects
    """
    deck = []
    for card_name in card_name_array:
        deck.append(create_card(card_name))
    return deck

def create_deck_from_csv(preset_path: str):
    """Method that creates a deck form a csv file of card names
        Args:
            preset_path: the path of the file that contains a card preset in csv
        Returns:
            a list containing Card objects
    """
    with open(preset_path, 'r') as csvfile:
        deck = []
        reader = csv.reader(csvfile)
        for row in reader:
            for name in row:
                deck.append(create_card(name))
        return deck


def monster_card_to_string(card: Monster):
    """
    :param: card: The card to convert to a string
    :return: A string in format {cardName} {attack}/{defense}
    """
    return "{cardName} {attack}/{defense}".format(cardName=card.name, attack=card.attack_points,
                                                  defense=card.attack_points)