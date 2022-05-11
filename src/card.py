import csv
from enum import Enum, unique
from typing import Callable
# from src.card_effects import Effect


class Card:
    """A class representing a Yu-Gi-Oh! Card.
    """
    def __init__(self, name: str, description: str):
        """Initializes the generic fields of a Yu-Gi-Oh! Card.

        Args:
            name: A string containing the name of the card.
            description: A string containing a Yu-Gi-Oh! card description.
        """
        self.name = name
        self.description = description

    def display_card(self) -> dict:
        """Gets the information for the current card.

        Returns:
            Dictionary containing the instance variables of the Card class.
            Gets the information for the current card.
        """
        return {"name": self.name, "description": self.description}


class Monster(Card):
    """A class representing a Yu-Gi-Oh! Monster Card.

    Note: This class only supports Normal monsters in the current build.
    """
    FACE_UP = 'up'
    FACE_DOWN = 'down'
    ATK = 'atk'
    DEF = 'def'

    def __init__(self, name: str, description: str, attribute: str, monster_type: str,
                 level: int, attack_points: int, defense_points: int):
        """Initializes the Monster class with the specified parameters.

        Args:
            name: A string containing the name of the monster card.
            description: A string containing a Yu-Gi-Oh! card description.
            attribute: A string containing the attribute of the monster (DARK LIGHT WATER FIRE EARTH WIND DIVINE).
            monster_type: A string containing the monster's type (Warrior, Beast-Warrior, Spellcaster, Fiend, etc.).
            level: An integer defining the level of the monster (Ranges from 1 to 12).
            attack_points: An integer defining the monster's attack points.
            defense_points: An integer defining the monster's defense points.
        """
        super().__init__(name, description)
        self.attribute = attribute
        self.base_atk = attack_points
        self.base_def = defense_points
        self.attack_points = attack_points
        self.defense_points = defense_points
        self.level = level
        self.monster_type = monster_type
        self.face_pos = Monster.FACE_UP
        self.battle_pos = Monster.ATK
        self.equipped_spell = None

    def __eq__(self, other_monster):
        """Determines whether two monster cards are equal.

        Args:
            other_monster: The monster variable we are comparing to

        Returns: True if the two cards are equal, False otherwise.
        """

        return isinstance(other_monster, Monster) and self.name == other_monster.name

    def __repr__(self):
        """
        Returns: string representing the card data.
        """
        str_repr = "name:%s, level:%d, attribute:%s, type:%s, atk:%d, def:%d, face position:%s, battle position:%s" % \
                   (self.name, self.level, self.attribute, self.monster_type, self.attack_points, self.defense_points,
                    self.face_pos, self.battle_pos)
        return str_repr

    def reset_stats(self):
        self.attack_points, self.defense_points = self.base_atk, self.base_def


class Spell:
    """A class representing a Yu-Gi-Oh! Spell Card.

    Note: This class only supports Normal and Equip spells in the current build.
    """
    @unique
    class Position(str, Enum):
        FACE_UP = 'up'
        FACE_DOWN = 'down'

    @unique
    class Icon(str, Enum):
        NORMAL = 'normal'
        EQUIP = 'equip'
        CONTINUOUS = 'continuous'
        FIELD = 'field'
        RITUAL = 'ritual'
        QUICK_PLAY = 'quick play'

    def __init__(self, name: str, icon: str, description: str, effect: Callable, effect_args: list):
        """Initializes the Spell class with the specified parameters.

        Args:
            name: A string containing the name of the spell card.
            icon: A string containing the type of the spell card.
            description: A string containing a Yu-Gi-Oh! card description.
            effect: A function that performs the effect of the spell.
            effect_args: Arguments for `effect` function.
        """
        self.name = name
        self.icon = Spell.Icon[icon.upper()]
        self.description = description
        self.speed = 2 if self.icon == Spell.Icon.QUICK_PLAY else 1
        self.position = Spell.Position.FACE_UP
        self.effect = effect
        self.effect_args = effect_args[:-1] if self.icon == Spell.Icon.EQUIP else effect_args
        self.required_monster_type = effect_args[-1] if self.icon == Spell.Icon.EQUIP else None
        self.equipped_monster = None

    def __eq__(self, other_spell):
        """Determines whether two spell cards are equal.

        Args:
            other_spell: The spell card we are comparing to.

        Returns: True if the two cards are equal, False otherwise.
        """

        return isinstance(other_spell, Spell) and self.name == other_spell.name

    def __repr__(self):
        """
        Returns: string representing the card data.
        """
        str_repr = "name:%s, icon:%s, speed:%d, position:%s" % (self.name, self.icon.value, self.speed,
                                                                self.position.value)
        return str_repr

    def activate_effect(self):
        if self.icon == Spell.Icon.EQUIP:
            self.effect(self.equipped_monster, *self.effect_args)
        else:
            self.effect(*self.effect_args)


def create_card(card_name: str, effect=None):
    """Creates a card based on the specified card_name.
    Args:
        card_name: The name of the card to be created.
        effect: Effect class used by spell cards.

    Returns: a Card type corresponding to the card_name, or None if no card exists with that name
    """
    with open('sources/cards.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0].lower().replace(" ", "") == card_name.lower().replace(" ", ""):
                if row[1] == "Monster":
                    return Monster(name=row[0], attribute=row[2], monster_type=row[3], level=int(row[4]),
                                   attack_points=int(row[5]), defense_points=int(row[6]), description=row[7])
                elif row[1] == "Spell":
                    def convert_type(arg):
                        return int(arg) if arg.isnumeric() or arg.lstrip('-').isnumeric() else arg

                    return Spell(name=row[0], icon=row[2], description=row[3], effect=getattr(effect, row[4].strip()),
                                 effect_args=[convert_type(arg) for arg in row[5:]])
        return None


def create_deck_from_array(card_name_array: list, effect=None):
    """Method that creates a deck given an array of strings of card names

    Args:
        card_name_array: an array of strings of card names to build the deck
        effect: Effect class used by spell cards.

    Returns:
        a list containing Card objects
    """
    return [create_card(card_name, effect) for card_name in card_name_array]


def create_deck_from_preset(preset_path: str):
    """Method that creates a deck form a csv file of card names.

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


def deck_to_card_name_list(cards: list):
    """Method to convert a list of Card objects to a list of their names only.

    Args:
        cards: A list of cards

    Returns:
        a list of card names
    """
    return [card.name for card in cards]


def monster_card_dict_to_card_object(card_dict: dict):
    """Method to convert a dictionary representation of a card to a card Object.

    Args:
        card_dict: a dict or json representation of a card

    Returns:
        a card object using the attributes in the card_dict
    """

    return Monster(name=card_dict["name"], description=card_dict["description"], attribute=card_dict["attribute"],
                   monster_type=card_dict["monster_type"], level=card_dict["level"],
                   attack_points=card_dict["attack_points"], defense_points=card_dict["defense_points"])


def monster_card_to_string(card: Monster):
    """
    Args:
        card: The card to convert to a string

    Returns:
        A string in format {cardName} {attack}/{defense}
    """
    return "{cardName} {attack}/{defense} {position} {level}*".format(cardName=card.name, attack=card.attack_points,
                                                                      defense=card.attack_points,
                                                                      position=card.battle_pos[0].upper(),
                                                                      level=card.level)

