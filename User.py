class User:
    def __init__(self, userID, userName, userEmail, userPassword, winCount, straightCount, 
                 flushCount, fullHouseCount, quadCount, straightFlushCount, royalFlushCount,
                 muckCount, blind2Count, blind4Count, tenFlopCount, tenCount, tenPreFlopCount, 
                 challengeCount, challengeDenyCount, flopPeekCount, playerPeekCount) -> None:
        
        self.userID = userID
        self.userName = userName
        self.userEmail = userEmail
        self.userPassword = userPassword
        self.winCount = winCount
        self.straightCount = straightCount
        self.flushCount = flushCount
        self.fullHouseCount = fullHouseCount
        self.quadCount = quadCount
        self.straightFlushCount = straightFlushCount
        self.royalFlushCount = royalFlushCount
        self.muckCount = muckCount
        self.blind2Count = blind2Count
        self.blind4Count = blind4Count
        self.tenFlopCount = tenFlopCount
        self.tenCount = tenCount
        self.tenPreFlopCount = tenPreFlopCount
        self.challengeCount = challengeCount
        self.challengeDenyCount = challengeDenyCount
        self.flopPeekCount = flopPeekCount
        self.playerPeekCount = playerPeekCount
        
    def getUserID(self):
        return self.userID
    
    def setUserID(self, value):
        self.userID = value
        
    def getUserName(self):
        return self.userName
    
    def setUserName(self, value):
        self.userName = value
        
    def getUserEmail(self):
        return self.userEmail
    
    def setUserEmail(self, value):
        self.userEmail = value
        
    def getUserPassword(self):
        return self.userPassword
    
    def setUserPassword(self, value):
        self.userPassword = value
        
    def getWinCount(self):
        return self.winCount
    
    def setWinCount(self, value):
        self.winCount = value
        
    def getStraightCount(self):
        return self.straightCount
    
    def setStraightCount(self, value):
        self.straightCount = value
        
    def getFlushCount(self):
        return self.flushCount
    
    def setFlushCount(self, value):
        self.flushCount = value
        
    def getFullHouseCount(self):
        return self.fullHouseCount
    
    def setFullHouseCount(self, value):
        self.fullHouseCount = value
        
    def getQuadCount(self):
        return self.quadCount
    
    def setQuadCount(self, value):
        self.quadCount = value
        
    def getStraightFlushCount(self):
        return self.straightFlushCount
    
    def setStraightFlushCount(self, value):
        self.straight

    def setRoyalFlushCount(self, royalFlushCount):
        self.royalFlushCount = royalFlushCount

    def getRoyalFlushCount(self):
        return self.royalFlushCount

    def setMuckCount(self, muckCount):
        self.muckCount = muckCount

    def getMuckCount(self):
        return self.muckCount

    def setBlind2Count(self, blind2Count):
        self.blind2Count = blind2Count

    def getBlind2Count(self):
        return self.blind2Count

    def setBlind4Count(self, blind4Count):
        self.blind4Count = blind4Count

    def getBlind4Count(self):
        return self.blind4Count

    def setTenFlopCount(self, tenFlopCount):
        self.tenFlopCount = tenFlopCount

    def getTenFlopCount(self):
        return self.tenFlopCount

    def setTenCount(self, tenCount):
        self.tenCount = tenCount

    def getTenCount(self):
        return self.tenCount

    def setTenPreFlopCount(self, tenPreFlopCount):
        self.tenPreFlopCount = tenPreFlopCount

    def getTenPreFlopCount(self):
        return self.tenPreFlopCount

    def setChallengeCount(self, challengeCount):
        self.challengeCount = challengeCount

    def getChallengeCount(self):
        return self.challengeCount

    def setChallengeDenyCount(self, challengeDenyCount):
        self.challengeDenyCount = challengeDenyCount

    def getChallengeDenyCount(self):
        return self.challengeDenyCount

    def setFlopPeekCount(self, flopPeekCount):
        self.flopPeekCount = flopPeekCount

    def getFlopPeekCount(self):
        return self.flopPeekCount

    def setPlayerPeekCount(self, playerPeekCount):
        self.playerPeekCount = playerPeekCount

    def getPlayerPeekCount(self):
        return self.playerPeekCount
