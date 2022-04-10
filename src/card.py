class Card:
    def __init__(self, name, description, card_type):
        self.name = name
        self.description = description
        self.card_type = card_type

    def display_card(self) -> dict:
        return {"name": self.name, "card_type": self.card_type, "description": self.description}


class Monster(Card):
    def __init__(self, name, description, attribute, monster_type, level, attackpoints, defensepoints):
        super().__init__(name, description, "Monster")
        self.attribute = attribute
        self.attackPoints = attackpoints
        self.defensePoints = defensepoints
        self.level = level
        self.monster_type = monster_type

    def display_card(self) -> dict:
        display_info = super().display_card()
        display_info["level"] = self.level
        display_info["attribute"] = self.attribute
        display_info["monster_type"] = self.monster_type
        display_info["ATK"] = self.attackPoints
        display_info["DEF"] = self.defensePoints
        return display_info
