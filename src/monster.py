from src.card import Card


class Monster(Card):
    def __init__(self, name, description, card_type, attack, defense):
        super(Monster, self).__init__(name, description, card_type)
        self.attack = attack
        self.defense = defense
        