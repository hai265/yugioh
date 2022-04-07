# Game manages the logic of the game, determines the winner of game if one player's health reaches 0,
# manages putting monsters on each player's field.
class Game:
    def __init__(self):
        self.players = []
        self.currentPlayersTurn = None
        self.field = []

    def determineFirstPlayer(self):
        pass

    def changeTurn(self):
        pass

    def attackMonster(self, attackingMonster, attackedMonster):
        pass

    def isThereWinner(self):
        pass

    def readGame(self):
        pass

    def summonMonster(self):
        pass

    def tributeSummonMonster(self):
        pass