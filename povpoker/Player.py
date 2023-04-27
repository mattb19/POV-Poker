class Player:
    def __init__(self, user, card1, card2, chipCount, blind) -> None:
        self.user = user
        self.card1 = card1
        self.card2 = card2
        self.chipCount = chipCount
        self.currentBet = 0
        self.blind = blind
        self.turn = False
        self.color = "white"
        self.allIn = False
        self.currentBetStr = ""
        self.totalValue = 0
        self.spectate = False
    
    
    def getBlind(self):
        return self.blind
    
    def setTotalValue(self, value):
        self.totalValue += value
        
    def setSpectate(self, value):
        self.spectate = value
    
    def getSpectate(self):
        return self.spectate
        
    def setTotalValueZero(self):
        self.totalValue = 0
    
    def getTotalValue(self):
        return self.totalValue
    
    def getColor(self):
        return self.color
    
    def getAllIn(self):
        return self.allIn
    
    def setAllIn(self, allIn):
        self.allIn = allIn
    
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
    
    def getCurrentBetStr(self):
        if self.currentBet == None or self.currentBet == "0":
            return ""
        return str(self.currentBetStr)