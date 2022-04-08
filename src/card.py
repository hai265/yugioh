class Card:
    def __init__(self, name, description, card_type):
        self.name = name
        self.description = description
        self.card_type = card_type


class Monster(Card):
    def __init__(self, name, description, attribute, attackpoints, defensepoints, level, monster_type):
        super().__init__(name, description, "monster")
        self.attribute = attribute
        self.attackPoints = attackpoints
        self.defensePoints = defensepoints
        self.level = level
        self.type = monster_type
