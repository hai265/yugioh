class Player:
    def __init__(self, lifepoints: int, name: str):
        self.lifePoints = lifepoints
        self.name = name
        self.deck = []
        self.hand = []
        self.graveyard = []
        self.field = []
    # Implement getters and setters
    # Draws a card from player's deck and add to hand
    def drawCard(self):
        pass
    def getHandSize(self):
        pass

    def getDeckSize(self):
        pass

    def getGraveyardSize(self):
        pass

    def summonMonster(self, handIndex: int, fieldIndex: int):
        pass

    def tributeSummon(self, handIndex: int, fieldIndex: int):
        pass

    def sendCardToGraveyard(self, fieldIndex, handIndex):
        pass

    def decreaseLifePoints(self, lifepoints):
        pass

