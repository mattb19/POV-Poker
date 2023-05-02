from Card import *


class CheckHands:


    def isRoyalFlush(self, cards1):
        cards = [i.getValue() for i in cards1]
        suits = sorted(cards1, key=lambda x:x.getSuit(), reverse=True)
        if ((cards[0]+1 == cards[1] and cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and 
        suits[0] == suits[1] and suits[1] == suits[2] and suits[2] == suits[3] and suits[3] == suits[4] and cards[4] == 14) or
        (cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5] and 
        suits[1] == suits[2] and suits[2] == suits[3] and suits[3] == suits[4] and suits[4] == suits[5] and cards[5] == 14) or
        (cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5] and cards[5]+1 == cards[6] and 
        suits[2] == suits[3] and suits[3] == suits[4] and suits[4] == suits[5] and suits[5] == suits[6] and cards[6] == 14)):
            return [True, 10000000000000000000000000000000000000]
        return [False, 0]


    def isStraightFlush(self, cards1):
        cards = [i.getValue() for i in cards1]
        suits = sorted(cards1, key=lambda x:x.getSuit(), reverse=True)
        cards.sort()
        sFlush = 0
        if (cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5] and cards[5]+1 == cards[6] and 
        suits[2] == suits[3] and suits[3] == suits[4] and suits[4] == suits[5] and suits[5] == suits[6]):
            sFlush = cards[6]
        elif (cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5] and 
        suits[1] == suits[2] and suits[2] == suits[3] and suits[3] == suits[4] and suits[4] == suits[5]):
            sFlush = cards[5]
        elif (cards[0]+1 == cards[1] and cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and 
        suits[0] == suits[1] and suits[1] == suits[2] and suits[2] == suits[3] and suits[3] == suits[4]):
            sFlush = cards[4]
        
        if sFlush == 0:
            return [False, 0]
        
        val = 90000000000 + sFlush
        
        return [True, val]


    def isQuads(self, cards):
        cardValues = [i.getValue() for i in cards]
        quads = 0
        for i in cardValues:
            if cardValues.count(i) == 4:
                quads = i
                cardValues.remove(i)
                cardValues.remove(i)
                cardValues.remove(i)
                cardValues.remove(i)
        if quads == 0:
            return [False,0]
        cardValues.sort()
        cardValues.reverse()
        
        h1 = cardValues[0]
        
        
        val = 80000000000 + quads*100000000 + h1*1000000

        return[True,val]


    def isFullHouse(self, cards):
        cardValues = [i.getValue() for i in cards]
        f1 = 0
        f1c = 0
        f2 = 0
        f2c = 0
        for i in cardValues:
            if f1 == 0 and cardValues.count(i) == 3:
                f1 = i
                f1c = cardValues.count(i)
                cardValues.remove(i)
                cardValues.remove(i)
                cardValues.remove(i)
            elif f2 == 0 and cardValues.count(i) >= 2:
                f2 = i
                f2c = cardValues.count(i)
        
        if f1 == 0 or f2 == 0:
            return [False, 0]
        
        if f1 < f2 and f1c == f2c:
            f1, f2 = f2, f1
        
        val = 70000000000 + f1*100000000 + f2*1000000
        return [True, val]
        
        


    def isFlush(self, cards):
        
        handSuits = [i.getSuit() for i in cards]
        flushSuit = ""
        for i in handSuits:
            if handSuits.count(i) == 5:
                flushSuit = i
                break
        if flushSuit == "":
            return [False,0]
        cardValues = [i.getValue() for i in cards if i.getSuit() == flushSuit]
        cardValues.sort()
        cardValues.reverse()
        h1 = cardValues[0]
        h2 = cardValues[1]
        h3 = cardValues[2]
        h4 = cardValues[3]
        h5 = cardValues[4]
        val = 60000000000 + h1*100000000 + h2*1000000 + h3*10000 + h4*100 + h5*1
        return [True,val]


    def isStraight(self, cards1):
        cards = [i.getValue() for i in cards1]
        cards.sort()
        straight = 0
        if cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5] and cards[5]+1 == cards[6]:
            straight = cards[6]
        elif cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5]:
            straight = cards[5]
        elif cards[0]+1 == cards[1] and cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4]:
            straight = cards[4]
        else:
            return [False,0]
        val = 50000000000 + straight*100000000 
        return[True,val]   


    def isTrips(self, cards):
        cardValues = [i.getValue() for i in cards]
        tripValue = 0 
        for i in cardValues:
            if cardValues.count(i) == 3:
                tripValue = i
                cardValues.remove(i)
                cardValues.remove(i)
                cardValues.remove(i)
        if tripValue == 0:
            return[False, 0]
        cardValues.sort()
        cardValues.reverse()
        h1 = cardValues[0]
        h2 = cardValues[1]
        
        val = 40000000000 + tripValue*100000000 + h1*1000000 + h2*10000
        return [True,val]
        
                
        

    def isTwoPair(self, cards):
        cardValues = [i.getValue() for i in cards]
        cardValues.sort()
        pair1 = 0
        pair2 = 0
        for i in cardValues:
            if cardValues.count(i) == 2 and pair1 == 0:
                pair1 += i
                cardValues.remove(i)
                cardValues.remove(i)
            elif cardValues.count(i) == 2 and pair2 == 0:
                pair2 += i
                cardValues.remove(i)
                cardValues.remove(i)
        if pair1 < pair2:
            pair1,pair2 = pair2,pair1
        cardValues.sort()    
        cardValues.reverse()
        h1 = cardValues[0]
        
        
        val = 30000000000 + pair1*100000000 + pair2*1000000 + h1*10000   
            
        
        if pair1 == 0 or pair2 == 0:
            return [False, 0]
        return [True,val]
        



    def isPair(self, cards):
        cardValues = [i.getValue() for i in cards]
        cardValues.sort()
        pairType = 0
        for i in cardValues:
            if cardValues.count(i) == 2:
                cardValues.remove(i)
                cardValues.remove(i)
                pairType = i
        if pairType == 0:
            return [False,0]
        cardValues.sort()
        cardValues.reverse()
        h1 = cardValues[0]
        h2 = cardValues[1]
        h3 = cardValues[2]
        
        val = 20000000000 + pairType*100000000 + h1*1000000 + h2*10000 + h3*100
        
        return [True, val]
                

    def isHighCard(self, cards):
        cardValues = [i.getValue() for i in cards]
        cardValues.sort()
        cardValues.reverse()
        h1 = cardValues[0]
        h2 = cardValues[1]
        h3 = cardValues[2]
        h4 = cardValues[3]
        h5 = cardValues[4]
        val = 10000000000 + h1*100000000 + h2*1000000 + h3*10000 + h4*100 + h5*1
        return [True,val]
        

        
        