import random
from Card import Card
import time
import Player

class Game:
    def __init__(self, players, smallBlind, bigBlind, active) -> None:
        self.players = players
        self.deck = []
        self.pot = 0
        self.currentBet = 0
        self.round = 0
        self.currentPlayer = 0
        self.tableCards = []
        self.lastWinners = []
        self.playerNames = [i.getUser() for i in self.players]
        self.playerCount = len(self.players)
        self.playerQueue = []
        self.active = active
        
        self.flop1 = Card("None","None",0)
        self.flop2 = Card("None","None",0)
        self.flop3 = Card("None","None",0)
        self.turn = Card("None","None",0)
        self.river = Card("None","None",0)
        
        self.smallBlind = smallBlind
        self.bigBlind = bigBlind
       
        
        
    
    def shuffleDeck(self):
        # generate a new deck
        suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        for i, suit in enumerate(suits):
            for j, num in enumerate(numbers):
                self.deck.append(Card(suit, num, values[j]))
                
        # shuffle deck 3 times
        random.shuffle(self.deck)
        random.shuffle(self.deck)
        random.shuffle(self.deck)


    def dealCards(self):
        # deal cards to players from a pre shuffled deck
        for i in range(0, len(self.players)):
            self.players[i].setCard1(self.deck[-1])
            self.deck.pop()
        for i in range(0, len(self.players)):
            self.players[i].setCard2(self.deck[-1])
            self.deck.pop()
        
        
    def newRound(self):
        # generate a new deck
        self.shuffleDeck()
        
        self.players + self.playerQueue
        self.playerQueue = []
        self.round = 0
        # rotates player list by 1
        
        
        # set everyones bet count to zero and turn to true
        for i in self.players:
            i.setCurrentBetZero()
            i.setTurn(True)
            i.setColor("white")
        
        # set blinds bet count
        self.players[0].setCurrentBet(self.smallBlind)
        self.players[0].setChipCount(0-self.smallBlind)
        self.players[1].setCurrentBet(self.bigBlind)
        self.players[1].setChipCount(0-self.bigBlind)
        self.currentBet = self.bigBlind
        self.pot = 0
        self.pot += self.bigBlind
        self.pot += self.smallBlind
        
        # set table cards to face down
        self.flop1 = Card("None","None",0)
        self.flop2 = Card("None","None",0)
        self.flop3 = Card("None","None",0)
        self.turn = Card("None","None",0)
        self.river = Card("None","None",0)
        
        # get dealt deck and playerlist with updated player hands
        self.dealCards()
        
        # determines flop, turn and river cards
        tableCards = []
        for i in range(0, len(self.deck)):
            if i in [0,1,2,4,6]:
                tableCards.append(self.deck[-1])
                self.deck.pop()
            else:
                self.deck.pop()
        self.tableCards = tableCards
        
        # get player 3, set him to bet first
        self.currentPlayer = 2
    
    
    def placeBetFold(self, value):
        # get current player
        x = self.currentPlayer
        player = self.players[x]
        
        # if they fold
        if value == None: 
            player.setFolded()
            player.setTurn(False)
            player.setColor("black")
            self.players[x] = player
            final = player.getUser()+" Folds."
        
        # if they check
        elif value == 0 and player.getCurrentBet() == self.currentBet:
            player.setTurn(False)
            self.players[x] = player
            final = player.getUser()+" Checks."
        
        # if they call
        elif value+player.getCurrentBet() == self.currentBet and value < player.getChipCount(): 
            player.setCurrentBet(value)
            player.setChipCount(0-value)
            player.setTurn(False)
            self.pot += value
            self.players[x] = player
            final = player.getUser()+" Calls "+str(value)+"!"
        
        # if they raise
        elif value >= self.currentBet and value < player.getChipCount():
            player.setCurrentBet(value)
            player.setChipCount(0-value)
            player.setTurn(False)
            self.currentBet = value
            self.pot += value
            self.players[x] = player
            final = player.getUser()+" Bets "+str(value)+"!"
        
        # if they go all in
        elif value == player.getChipCount():
            player.setCurrentBet(value)
            player.setChipCount(0-value)
            player.setTurn(False)
            player.setColor("#EE4B2B")
            self.pot += value
            self.currentBet = value
            self.players[x] = player
            final = player.getUser()+" IS ALL IN! "
        
        # if they don't bet enough
        elif value < self.currentBet:
            final = "You must put more in to call or raise"
        
        # if they put in too much
        elif value > player.getChipCount():
            final = "Insufficient Funds"
        
        # set turn to true for all players who havent folded or called new bet
        for i in self.players:
            if i.getCurrentBet() == None:
                continue
            elif value == None:
                continue
            elif i.getCurrentBet() < value:
                i.setTurn(True)
                
        # determine who goes next
        self.whoGoesNext()
        
        
    def whoGoesNext(self): 
        # if its pre flop
        if self.round == 0:
            turns = [i.getTurn() for i in self.players]
            
            # if all players have called, checked or folded
            if True not in turns:
                self.currentPlayer = 0
                self.currentBet = 0
                self.round += 1
                self.flop1 = self.tableCards[0]
                self.flop2 = self.tableCards[1]
                self.flop3 = self.tableCards[2]
                
                # set all players current bets to zero
                for i in self.players:
                    if i.getCurrentBet() is not None:
                        i.setCurrentBetZero()
                        i.setTurn(True)
                        i.setColor("white")
                return self.currentPlayer
            
            # determine who's turn is next
            counter = self.currentPlayer
            while True:
                if counter == len(self.players)-1:
                    if turns[0] == False:
                        counter = 0
                        continue
                    elif turns[0] == True:
                        self.currentPlayer = 0
                        return self.currentPlayer
                    continue
                elif turns[counter+1] == False:
                    counter += 1
                    continue
                elif turns[counter+1] == True:
                    counter += 1
                    self.currentPlayer = counter
                    return self.currentPlayer        
        
        # if the flop is down
        elif self.round == 1:
            turns = [i.getTurn() for i in self.players]
            
            # if all players have called, checked or folded
            if True not in turns:
                self.currentPlayer = 0
                self.currentBet = 0
                self.round += 1
                self.turn = self.tableCards[3]
                for i in self.players:
                    if i.getCurrentBet() is not None:
                        i.setCurrentBetZero()
                        i.setTurn(True)
                        i.setColor("white")
                return self.currentPlayer
            
            # determine who's turn is next
            counter = self.currentPlayer
            while True:
                if counter == len(self.players)-1:
                    self.currentPlayer = turns.index(True)
                    return self.currentPlayer
                elif turns[counter+1] == False:
                    counter += 1
                    continue
                elif turns[counter+1] == True:
                    counter += 1
                    self.currentPlayer = counter
                    return self.currentPlayer
                
        # if the turn is down
        elif self.round == 2:
            turns = [i.getTurn() for i in self.players]
            if True not in turns:
                self.currentPlayer = 0
                self.currentBet = 0
                self.round += 1
                self.river = self.tableCards[4]
                for i in self.players:
                    if i.getCurrentBet() is not None:
                        i.setCurrentBetZero()
                        i.setTurn(True)
                        i.setColor("white")
                return self.currentPlayer
            counter = self.currentPlayer
            while True:
                if counter == len(self.players)-1:
                    self.currentPlayer = turns.index(True)
                    return self.currentPlayer
                elif turns[counter+1] == False:
                    counter += 1
                    continue
                elif turns[counter+1] == True:
                    counter += 1
                    self.currentPlayer = counter
                    return self.currentPlayer

        # if the river is down
        elif self.round == 3:
            turns = [i.getTurn() for i in self.players]
            if True not in turns:
                self.currentPlayer = 0
                for i in self.players:
                    if i.getCurrentBet() is not None:
                        i.setCurrentBetZero()
                        i.setColor("white")
                return self.endRound()
            counter = self.currentPlayer
            while True:
                if counter == len(self.players)-1:
                    self.currentPlayer = turns.index(True)
                    return self.currentPlayer
                elif turns[counter+1] == False:
                    counter += 1
                    continue
                elif turns[counter+1] == True:
                    counter += 1
                    self.currentPlayer = counter
                    return self.currentPlayer
          
                
    def endRound(self):
        finalPlayers = [i for i in self.players if i.getCurrentBet() is not None]
        for i in finalPlayers:
            lst = [self.flop1, self.flop2, self.flop3, self.turn, self.river, i.getCard1(), i.getCard2()]
            unsortedCards = [[i.getValue(), i.getSuit()] for i in lst]
            card = sorted(unsortedCards,key=lambda l:l[0])
            cards = [int(i[0]) for i in card]
            suits = [i[1] for i in card]
            # for j in lst:
                # print(j)
                
            
            quads = 0
            for j in cards:
                if cards.count(j) == 4:
                    quads = j
            
            o = 0
            t = 0
            fullHouse = []
            for j in cards:
                if cards.count(j) == 3 and j > o:
                    o = j
                elif cards.count(j) == 2 and j > t:
                    t = j
            if t != 0 and o != 0:
                fullHouse.append(o)
                fullHouse.append(t)
            
            
            trips = 0
            one = 0
            two = 0
            for j in cards:
                if cards.count(j) == 3 and j > trips:
                    trips = j
            if trips != 0:
                newCards = [i for i in cards if i != trips]
                newCards.reverse()
                one = newCards[0]
                two = newCards[1]
            
        
            card5 = 0
            twoPair = []
            twowee = []
            for j in cards:
                if cards.count(j) == 2 and j not in twowee:
                    twowee.append(j)
            if len(twowee) >= 2:
                twowee.sort()
                twowee.reverse()
                twoPair.append(twowee[0])
                twoPair.append(twowee[1])
                twoPair.sort()
                newCards = [i for i in cards if i not in twowee]
                card5 = max(newCards)
            
            
            
            pair = 0
            otherCards = []
            for j in cards:
                if cards.count(j) == 2 and j > pair:
                    pair = j
            if pair != 0:
                newCards = [i for i in cards if i != pair]
                newCards.reverse()
                otherCards.append(newCards[0])
                otherCards.append(newCards[1])
                otherCards.append(newCards[2])
            
            
            highCards = []
            newCards = [i for i in cards]
            newCards.reverse()
            newCards.pop()
            newCards.pop()
            highCards = newCards
            

            
            
            
            
            
            # royal flush check
            if ((cards[0]+1 == cards[1] and cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and 
                suits[0] == suits[1] and suits[1] == suits[2] and suits[2] == suits[3] and suits[3] == suits[4] and cards[4] == 14) or
                (cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5] and 
                suits[1] == suits[2] and suits[2] == suits[3] and suits[3] == suits[4] and suits[4] == suits[5] and cards[5] == 14) or
                (cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5] and cards[5]+1 == cards[6] and 
                suits[2] == suits[3] and suits[3] == suits[4] and suits[4] == suits[5] and suits[5] == suits[6] and cards[6] == 14)):
                
                i.setCurrentBet(10000000000000000000)
            
            # straight flush check
            elif ((cards[0]+1 == cards[1] and cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and 
                suits[0] == suits[1] and suits[1] == suits[2] and suits[2] == suits[3] and suits[3] == suits[4]) or
                (cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5] and 
                suits[1] == suits[2] and suits[2] == suits[3] and suits[3] == suits[4] and suits[4] == suits[5]) or
                (cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5] and cards[5]+1 == cards[6] and 
                suits[2] == suits[3] and suits[3] == suits[4] and suits[4] == suits[5] and suits[5] == suits[6])):
                
                if cards[4]-cards[0] == 4:
                    x = 9000000+cards[4]+cards[3]+cards[2]+cards[1]+cards[0]
                    i.setCurrentBet(x)
                elif cards[5]-cards[1] == 4:
                    x = 9000000+cards[5]+cards[4]+cards[3]+cards[2]+cards[1]
                    i.setCurrentBet(x)
                elif cards[6]-cards[2] == 4:
                    x = 9000000+cards[6]+cards[5]+cards[4]+cards[3]+cards[2]
                    i.setCurrentBet(x)

            # quads check
            elif quads != 0:
                x = 8000000+(quads*4)
                i.setCurrentBet(x)
            
            # full house check
            elif len(fullHouse) != 0:
                x = 7000000+(fullHouse[0]*10000)+(fullHouse[1]*100)
                i.setCurrentBet(x)
            
            # flush check
            elif suits.count("Hearts") == 5 or suits.count("Spades") == 5 or suits.count("Diamonds") == 5 or suits.count("Clubs") == 5:
                x = 0
                if suits.count("Hearts") == 5:
                    flush = [i for i in card if i[1] == "Hearts"]
                    flushCount = [i[0] for i in flush]
                    x = 6000000+max(flushCount)
                elif suits.count("Spades") == 5:
                    flush = [i for i in card if i[1] == "Spades"]
                    flushCount = [i[0] for i in flush]
                    x = 6000000+max(flushCount)
                elif suits.count("Diamonds") == 5:
                    flush = [i for i in card if i[1] == "Diamonds"]
                    flushCount = [i[0] for i in flush]
                    x = 6000000+max(flushCount)
                elif suits.count("Clubs") == 5:
                    flush = [i for i in card if i[1] == "Clubs"]
                    flushCount = [i[0] for i in flush]
                    x = 6000000+max(flushCount)
                i.setCurrentBet(x)
            
            # straight check
            elif ((cards[0]+1 == cards[1] and cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4]) or
                (cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5]) or
                (cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5] and cards[5]+1 == cards[6])):
                if cards[4]-cards[0] == 4:
                    x = 5000000+cards[4]+cards[3]+cards[2]+cards[1]+cards[0]
                    i.setCurrentBet(x)
                elif cards[5]-cards[1] == 4:
                    x = 5000000+cards[5]+cards[4]+cards[3]+cards[2]+cards[1]
                    i.setCurrentBet(x)
                elif cards[6]-cards[2] == 4:
                    x = 5000000+cards[6]+cards[5]+cards[4]+cards[3]+cards[2]
                    i.setCurrentBet(x)
            
            # trips check
            elif trips != 0:
                x = 4000000 + (trips*10000) + one*100 + two*10
                i.setCurrentBet(x)
            
            # two pair check
            elif len(twoPair) != 0:
                x = 3000000 + (twoPair[0]*10000) + (twoPair[1]*100) + card5
                i.setCurrentBet(x)
            
            # pair check
            elif pair != 0:
                x = 2000000 + pair*10000 + otherCards[0]*1000 + otherCards[1]*100 + otherCards[2]*10
                i.setCurrentBet(x)
                
            # high card check
            else:
                x = highCards[0]*10000 + highCards[1]*1000 + highCards[2]*100 + highCards[3]*10 + highCards[4]*1
                i.setCurrentBet(x)
            
            # print(i.getUser())
            # print(i.getCurrentBet())
            # print()
            # print()
            # print()
        
        
        # check who won the hand
        winner = []
        high = 0
        for i in finalPlayers:
            if i.getCurrentBet() > high:
                if len(winner) != 0:
                    winner.clear()
                high = i.getCurrentBet()
                winner.append(i)
            elif i.getCurrentBet() == high:
                winner.append(i)
        winners = []
        for i in winner:
            winners.append([i, i.getCurrentBet()])
        for i in winners:
            i[0].setChipCount(self.pot//len(winners))
        self.lastWinners = winners
        print(self.players)
        print(self.round)
        print(self.lastWinners)
        print(self.currentPlayer)
        self.newRound()


    def gay(self):
        self.newRound()
        self.placeBetFold(20)
        
        self.placeBetFold(20)
        
        self.placeBetFold(20)
        
        self.placeBetFold(20)
        
        self.placeBetFold(20)
        self.placeBetFold(20)
        self.placeBetFold(20)
        self.placeBetFold(20)
        
        self.placeBetFold(10)
        
        self.placeBetFold(0)
        
        
        # flop test
        self.placeBetFold(0)
        self.placeBetFold(0)
        self.placeBetFold(0)
        self.placeBetFold(0)
        
        self.placeBetFold(0)
        
        self.placeBetFold(0)
        
        self.placeBetFold(0)
        
        self.placeBetFold(0)
        
        self.placeBetFold(0)
        
        self.placeBetFold(0)
        
        
        # turn test
        self.placeBetFold(0)
        self.placeBetFold(0)
        self.placeBetFold(0)
        self.placeBetFold(0)
        
        self.placeBetFold(0)
        
        self.placeBetFold(0)
        
        self.placeBetFold(0)
        self.placeBetFold(0)
        
        self.placeBetFold(0)
        
        self.placeBetFold(0)
        
        
        # river test
        self.placeBetFold(0)
        self.placeBetFold(0)
        self.placeBetFold(0)
        self.placeBetFold(0)
        
        self.placeBetFold(0)
        
        self.placeBetFold(0)
        
        self.placeBetFold(0)

        self.placeBetFold(0)

        self.placeBetFold(0)

        self.placeBetFold(0)
        
    
    def getPlayers(self):
        return self.players
    
    def getCurrentBet(self):
        return self.currentBet

    def getPot(self):
        return self.pot
    
    def getFlop1(self):
        return self.flop1
    
    def getFlop2(self):
        return self.flop2
    
    def getFlop3(self):
        return self.flop3
    
    def getTurn(self):
        return self.turn
    
    def getRiver(self):
        return self.river
    
    def getCurrentPlayer(self):
        return self.currentPlayer
    
    def getPlayerNames(self):
        return self.playerNames
    
    def getPlayerCount(self):
        return self.playerCount
    
    def addPlayers(self, name, chipCount):
        self.playerQueue.append(Player(name, None, None, chipCount, len(self.players)+len(self.playerQueue)-1, None))
    
    def isActive(self):
        return self.active
    
    def reset(self, big, small, player1, player2, player3):
        self.bigBlind = big
        self.smallBlind = small
        self.players = []
        self.deck = []
        self.pot = 0
        self.currentBet = 0
        self.round = 0
        self.currentPlayer = 0
        self.tableCards = []
        self.lastWinners = []
        self.playerNames = [i.getUser() for i in self.players]
        self.playerCount = len(self.players)
        self.playerQueue = []
        self.active = True
        self.flop1 = Card("None","None",0)
        self.flop2 = Card("None","None",0)
        self.flop3 = Card("None","None",0)
        self.turn = Card("None","None",0)
        self.river = Card("None","None",0)
        