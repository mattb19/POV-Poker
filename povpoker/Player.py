class Player:
    def __init__(self, user, card1, card2, chipCount, blind, currentBet=0, handWorth=0, turn=False, color="white", allIn=False, 
                 currentBetStr="", totalValue=0, spectate=False, muck=False, playerNum=0) -> None:
        self.user = user.strip(' ')
        self.card1 = card1
        self.card2 = card2
        self.chipCount = chipCount
        self.currentBet = currentBet
        self.blind = blind
        self.handWorth = handWorth
        self.turn = turn
        self.color = color
        self.allIn = allIn
        self.currentBetStr = currentBetStr
        self.totalValue = totalValue
        self.spectate = spectate
        self.muck = muck
        self.playerNum = playerNum
        
    
    def getMuck(self):
        return self.muck
    
    def setMuck(self, muck):
        self.muck = muck
    
    def getHandWorth(self):
        return self.handWorth

    
    
    def setHandWorth(self,Worth):
        self.handWorth = Worth
        
    def setHandWorthZero(self):
        self.handWorth = 0
        
    def getBlind(self):
        return self.blind
    
    def getHandWorth(self):
        return self.handWorth
    
    def setHandWorth(self, value):
        self.handWorth = value
    
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