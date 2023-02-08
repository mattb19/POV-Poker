class Player:
    def __init__(self, user, card1, card2, chipCount, playerNum, blind) -> None:
        self.user = user
        self.card1 = card1
        self.card2 = card2
        self.chipCount = chipCount
        self.currentBet = 0
        self.playerNum = playerNum
        self.blind = blind
        self.turn = False
        self.color = "white"
    
    def getBlind(self):
        return self.blind
    
    def getColor(self):
        return self.color
    
    def setColor(self, color):
        self.color = str(color)
    
    def setBlind(self, blind):
        self.blind = blind
        
    def getTurn(self):
        return self.turn
    
    def setTurn(self, turn):
        self.turn = turn
    
    def getUser(self):
        return str(self.user)
    
    def setUser(self, user):
        self.user = user

    def setCard1(self, user):
        self.card1 = user

    def getCard1(self):
        return self.card1

    def setCard2(self, hand):
        self.card2 = hand
    
    def getCard2(self):
        return self.card2

    def getChipCount(self):
        return self.chipCount

    def setChipCount(self, chipCount):
        self.chipCount += chipCount

    def getCurrentBet(self):
        return self.currentBet

    def setCurrentBet(self, currentBet):
        self.currentBet += currentBet
    
    def setCurrentBetZero(self):
        self.currentBet = 0
    
    def setFolded(self):
        self.currentBet = None

    def getPlayerNum(self):
        return self.playerNum

    def setPlayerNum(self, playerNum):
        self.playerNum = playerNum