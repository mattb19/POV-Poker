import random
from Card import Card
import time
from Player import Player
import json
from copy import deepcopy
from checkHands import CheckHands

class Game:
    def __init__(self, gameID, players, smallBlind, bigBlind, deck=[], pot=0, currentBet=0, round=0, currentPlayer=None, tableCards=[], lastWinners=[], 
                 playerNames=[], playerCount=0,  playerQueue=[], active=False, blinds=[], buyIn=1000, flip=True, running=False, abilities="ON", style="TEXAS HOLD'EM", bombPot=False, 
                 flop1=Card("None", "None", 0), flop2=Card("None", "None", 0), flop3=Card("None", "None", 0), turn=Card("None", "None", 0), river=Card("None", "None", 0), Time=0) -> None:
        self.gameID = gameID
        self.players = players
        self.deck = deck
        self.pot = pot
        self.currentBet = currentBet
        self.round = round
        self.currentPlayer = currentPlayer
        self.tableCards = tableCards
        self.lastWinners = lastWinners
        self.playerNames = [i.getUser().strip(' ') for i in self.players]
        self.playerCount = len(self.players)
        self.playerQueue = playerQueue
        self.active = active
        self.blinds = blinds
        self.buyIn = buyIn
        self.flip = flip
        self.running = running
        self.abilities = abilities
        self.style = style
        
        self.bombPot = bombPot
        
        self.flop1 = flop1
        self.flop2 = flop2
        self.flop3 = flop3
        self.turn = turn
        self.river = river
        
        self.smallBlind = smallBlind
        self.bigBlind = bigBlind
        
        self.Time = Time
       
        
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
        e = [i.getChipCount() for i in self.players]
        
        # set all players hand worth to 0
        for i in self.players:
            i.setHandWorthZero()
        
        self.shuffleDeck()
        
        # add any waiting players
        self.players += self.playerQueue
        self.playerQueue = []
        
        self.round = 0
        self.running = False
        
        for i in self.players:
            if i.getChipCount() == 0:
                i.setSpectate(True)
                i.setAllIn(False)
        
        # initialize blinds if its a new game
        if not self.active:
            self.players[0].setBlind(1)
            self.players[1].setBlind(2)
            for i in range(len(self.players)):
                self.players[i].setPlayerNum(i)
            self.active = True
        else:
            # rotate blinds
            for i in range(len(self.players)):
                if self.players[i].getBlind() == 0:
                    continue
                elif self.players[i].getBlind() == 1 and i == len(self.players)-1:
                    self.players[len(self.players)-1].setBlind(0)
                    self.players[0].setBlind(1)
                    self.players[1].setBlind(2)
                    break
                elif self.players[i].getBlind() == 1 and i == len(self.players)-2:
                    self.players[len(self.players)-2].setBlind(0)
                    self.players[len(self.players)-1].setBlind(1)
                    self.players[0].setBlind(2)
                    break
                else:
                    self.players[i].setBlind(0)
                    self.players[i+1].setBlind(1)
                    self.players[i+2].setBlind(2)
                    break
            
        
        # set everyones bet count to zero and turn to true
        for i in self.players:
            if i.getSpectate() == False:
                i.setCurrentBetZero()
                i.setTurn(True)
                i.setColor("white")
                i.setTotalValueZero()
                i.setAllIn(False)
            else:
                i.setFolded()
        
        
        # set blinds bet count
        self.pot = 0
        for i in range(len(self.players)):
            if self.players[i].getSpectate() == False:
                if self.players[i].getBlind() == 1:
                    self.players[i].setCurrentBet(self.smallBlind)
                    self.players[i].setChipCount(-self.smallBlind)
                    self.players[i].setTotalValue(self.smallBlind)
                    self.pot += self.smallBlind
                elif self.players[i].getBlind() == 2:
                    self.players[i].setCurrentBet(self.bigBlind)
                    self.players[i].setChipCount(-self.bigBlind)
                    self.players[i].setTotalValue(self.bigBlind)
                    self.pot += self.bigBlind

        self.currentBet = self.bigBlind
        
        # set table cards to face down
        self.flop1 = Card("None","None",0)
        self.flop2 = Card("None","None",0)
        self.flop3 = Card("None","None",0)
        self.turn = Card("None","None",0)
        self.river = Card("None","None",0)
        
        # get dealt deck and playerlist with updated player hands
        self.dealCards()
        
        # reset winners
        self.lastWinners = []
        
        # determines flop, turn and river cards
        tableCards = []
        for i in range(0, len(self.deck)):
            if i in [0,1,2,4,6]:
                tableCards.append(self.deck[-1])
                self.deck.pop()
            else:
                self.deck.pop()
        self.tableCards = tableCards
        
        nonFolded = [i.getSpectate() for i in self.players]
        # get player 3, set him to bet first
        for i in range(len(self.players)):
            if self.players[i].getBlind() == 2 and i < len(self.players)-1:
                counter = i+1
                while True:
                    if counter == len(self.players)-1:
                        if self.players[counter].getSpectate() == False:
                            self.currentPlayer = counter
                            break
                        else:
                            counter = 0
                    else:
                        if self.players[counter].getSpectate() == False:
                            self.currentPlayer = counter
                            break
                        else:
                            counter += 1
            elif self.players[i].getBlind() == 2 and i == len(self.players)-1:
                self.currentPlayer = nonFolded.index(False)
        
        if self.bombPot:
            # sleep for ui 
            time.sleep(5)
            for i in range(len(self.players)):
                if self.players[i].getSpectate() == False:
                    if self.players[i].getBlind == 2:
                        self.placeBetFold((.10*1000))
                    elif self.players[i].getBlind == 1:
                        self.placeBetFold((.10*1000))
                    else:
                        self.placeBetFold((.10*1000))
        
    
    def placeBetFold(self, value):
        if self.round == 4 or self.active == False:
            print("Error, invalid time to bet")
            return "Error: Invalid Bet Time"

        
        # get current player
        x = self.currentPlayer
        player = self.players[x]
        # if they fold
        if value == None: 
            player.setFolded()
            player.setTurn(False)
            player.setColor("white")
            self.players[x] = player
            final = player.getUser()+" Folds."
        
        # if they check
        elif value == 0 and player.getCurrentBet() == self.currentBet:
            player.setTurn(False)
            self.players[x] = player
            final = player.getUser()+" Checks."
        
        # if they call
        elif value == self.currentBet and value < player.getChipCount():
            player.setChipCount(0-(value-player.getCurrentBet()))
            player.setTurn(False)
            player.setTotalValue(value-player.getCurrentBet())
            self.pot += value-player.getCurrentBet()
            self.players[x] = player
            final = player.getUser()+" Calls "+str(value)+"!"
            player.setCurrentBet(value-player.getCurrentBet())
        
        # if they raise
        elif value > self.currentBet and value < player.getChipCount():
            player.setChipCount(0-(value-player.getCurrentBet()))
            player.setTurn(False)
            player.setTotalValue(value-player.getCurrentBet())
            self.currentBet = value
            self.pot += (value-player.getCurrentBet())
            self.players[x] = player
            player.setCurrentBet(value-player.getCurrentBet())
            final = player.getUser()+" Bets "+str(value)+"!"
        
        # if they go all in
        elif value-player.getCurrentBet() == player.getChipCount():
            player.setTotalValue(value-player.getCurrentBet())
            player.setChipCount(0-(value-player.getCurrentBet()))
            player.setTurn(False)
            player.setColor("#EE4B2B")
            self.pot += (value-player.getCurrentBet())
            if value >= self.currentBet:
                self.currentBet = value
            self.players[x] = player
            self.players[x].setAllIn(True)
            player.setCurrentBet(value-player.getCurrentBet())
            final = player.getUser()+" IS ALL IN! "
                
        
        # if they don't bet enough
        elif value+player.getCurrentBet() < self.currentBet:
            return "You must put more in to call or raise"
        
        # if they put in too much
        elif value > player.getChipCount():
            return "Insufficient Funds"
        
        # set turn to true for all players who havent folded or called new bet
        for i in self.players:
            if i.getCurrentBet() == None:
                continue
            elif value == None:
                continue
            elif i.getCurrentBet() < value and i.getAllIn() == False:
                i.setTurn(True)
        
        print(final)
                
        # determine who goes next
        self.whoGoesNext()
        
        
    def whoGoesNext(self): 
        turns = [i.getTurn() for i in self.players]
        
        # if all players have folded/all-in'd except one
        currentPlayers = [i for i in self.players if i.getCurrentBet() != None]

        if len(currentPlayers) == 1:
            # increment round
            self.round = 4
            return self.endRound()
        
        # if all players still in are all in
        allinPlayers = [i for i in self.players if i.getAllIn() == True]
        nonFolded = [i for i in self.players if i.getCurrentBet() != None]
        if (len(allinPlayers) == len(nonFolded)) or (len(allinPlayers)+1 == len(nonFolded) and True not in turns):
            while self.round < 4:
                if self.round == 0:
                    self.flop1 = self.tableCards[0]
                    self.flop2 = self.tableCards[1]
                    self.flop3 = self.tableCards[2]
                    self.running = True
                    self.round = 1
                    time.sleep(5)
                    for i in self.players:
                        if i.getSpectate() == False and i.getCurrentBet() is not None:
                            i.setCurrentBetZero()
                elif self.round == 1:
                    self.turn = self.tableCards[3]
                    self.round += 1
                    self.running = True
                    time.sleep(5)
                    for i in self.players:
                        if i.getSpectate() == False and i.getCurrentBet() is not None:
                            i.setCurrentBetZero()
                elif self.round == 2:
                    self.river = self.tableCards[4]
                    self.round += 1
                    self.running = True
                    time.sleep(5)
                    for i in self.players:
                        if i.getSpectate() == False and i.getCurrentBet() is not None:
                            i.setCurrentBetZero()
                elif self.round == 3:
                    self.round = 4
                    self.running = True
                    return self.endRound()
        
    
        # if all players have called, checked or folded
        if True not in turns:
            if self.bombPot and self.round == 0:
                self.bombPot = False
                # sleep for ui
                time.sleep(5)
            
            
            l = [i.getBlind() for i in self.players]
            blindIndex = l.index(1)
            c = blindIndex
            while True:
                if self.players[c].getCurrentBet() != None and self.players[c].getAllIn() == False:
                    break
                else:
                    if c == len(self.players)-1:
                        c = 0
                    else:
                        c += 1

            # sleep for ui changes on frontend
            self.currentPlayer = c
            self.currentBet = 0

            if self.round == 0:
                self.flop1 = self.tableCards[0]
                self.flop2 = self.tableCards[1]
                self.flop3 = self.tableCards[2]
            elif self.round == 1:
                self.turn == self.tableCards[3]
            elif self.round == 2:
                self.river == self.tableCards[4]
                

            
            # if its the last rotation, end the round
            if self.round == 3:
                for i in self.players:
                    if i.getCurrentBet() is not None and i.getAllIn() != True:
                        i.setColor("white")
                    if i.getSpectate() == False and i.getCurrentBet() is not None:
                        i.setCurrentBetZero()
                
                # increment round
                self.round = 4
                return self.endRound()

            self.round += 1
            

            
            # set all non-folded/all-in'd players current bets to zero
            for i in self.players:
                if i.getCurrentBet() is not None and i.getAllIn() == False and i.getSpectate() == False:
                    i.setCurrentBetZero()
                    i.setTurn(True)
                    i.setColor("white")
                elif i.getAllIn() == True:
                    i.setCurrentBetZero()
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
          
                
    def endRound(self):
        finalPlayers = [i for i in self.players if i.getCurrentBet() is not None]
        
        check = CheckHands()
        
        for i in finalPlayers:
            cards = [self.tableCards[0], self.tableCards[1], self.tableCards[2], self.tableCards[3], self.tableCards[4], i.getCard1(), i.getCard2()]
            cards = [Card(**i) for i in cards]

            if check.isRoyalFlush(cards)[0]:
                worth = check.isRoyalFlush(cards)[1]
                i.setHandWorth(worth)
                
            elif check.isStraightFlush(cards)[0]:
                worth = check.isStraightFlush(cards)[1]
                i.setHandWorth(worth)
                
            elif check.isQuads(cards)[0]:
                worth = check.isQuads(cards)[1]
                i.setHandWorth(worth)
                
            elif check.isFullHouse(cards)[0]:
                worth = check.isFullHouse(cards)[1]
                i.setHandWorth(worth)
                
            elif check.isFlush(cards)[0]:
                worth = check.isFlush(cards)[1]
                i.setHandWorth(worth)
                
            elif check.isStraight(cards)[0]:
                worth = check.isStraight(cards)[1]
                i.setHandWorth(worth)
                
            elif check.isTrips(cards)[0]:
                worth = check.isTrips(cards)[1]
                i.setHandWorth(worth)
                
            elif check.isTwoPair(cards)[0]:
                worth = check.isTwoPair(cards)[1]
                i.setHandWorth(worth)
                
            elif check.isPair(cards)[0]:
                worth = check.isPair(cards)[1]
                i.setHandWorth(worth)
                
            elif check.isHighCard(cards)[0]:
                worth = check.isHighCard(cards)[1]
                i.setHandWorth(worth)
                
            
            
        newList = sorted(finalPlayers, key=lambda x:x.getHandWorth(), reverse=True)
        disWinnings = []
        
        # Determine who wins what
        for i in newList:
            splitCount = 1
            
            # Determine how many people need to split it with
            if len(finalPlayers) == 1:
                disWinnings.append([i, self.pot])
                self.lastWinners.append(i.getUser())
                break
            
            for x in range(len(newList)):
                if newList[x].getHandWorth() == newList[x+1].getHandWorth():
                    splitCount += 1
                    break
                else:
                    break

            # determine what they win
            amount = 0
            for j in self.players:
                if i.getUser() != j.getUser():
                    if (j.getHandWorth() is None or i.getHandWorth() > j.getHandWorth()):
                        if (i.getTotalValue()//splitCount) >= (j.getTotalValue()//splitCount):
                            amount += (j.getTotalValue()//splitCount)
                            j.setTotalValue(-(j.getTotalValue()//splitCount))
                            self.pot -= (j.getTotalValue()//splitCount)
                        else:
                            amount += (i.getTotalValue()//splitCount)
                            j.setTotalValue(-(i.getTotalValue()//splitCount))
                            self.pot -= (j.getTotalValue()//splitCount)
            amount += i.getTotalValue()
            disWinnings.append([i, amount])
            if amount != 0:
                self.lastWinners.append(i.getUser())

        # set all players current bets to zero
        for j in self.players:
            if j.getSpectate() == False:
                j.setCurrentBetZero()
        
        self.currentPlayer = None
                
        # Distribute winnings
        for i in disWinnings:
            self.players[self.players.index(i[0])].setChipCount(i[1])

        
    def getGameID(self):
        return self.gameID
    
    def getRound(self):
        return self.round
    
    def getPlayers(self):
        return self.players
    
    def getCurrentBet(self):
        return self.currentBet

    def getPot(self):
        return self.pot

    def getCurrentPlayer(self):
        return self.currentPlayer
    
    def getPlayerNames(self):
        return self.playerNames

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
    
    def getActive(self):
        return self.active

    def setFlop1(self, card):
        self.flop1 = card
    
    def getAbilities(self):
        return self.abilities
    
    def getBuyIn(self):
        return self.buyIn
    
    def getBlinds(self):
        return str(self.bigBlind)+"/"+str(self.smallBlind)
    
    def getStyle(self):
        return self.style
    
    def setTime(self, Time):
        self.Time = Time
        
    def getTime(self):
        return self.Time
        
    def setFlop2(self, card):
        self.flop2 = card
        
    def setFlop3(self, card):
        self.flop3 = card
        
    def setTurn(self, card):
        self.turn = card
        
    def setRiver(self, card):
        self.river = card
    
    def getPlayerCount(self):
        return str(len(self.players)+len(self.playerQueue))+"/10"
    
    def getPlayerCountInt(self):
        return len(self.players)
    
    def setTableCards(self):
        self.tableCards = [i for i in self.tableCards]

    def setGameID(self, gameID):
        self.gameID = gameID
        
    def setPlayers(self, players):
        self.players = players
    
    def addPlayer(self, name):
        if self.active:
            print(self.playerNames)
            if len(self.players) <= 10 and name not in self.playerNames:
                self.players.append(Player(name,'../static/PNG-cards-1.3/None_of_None.png', '../static/PNG-cards-1.3/None_of_None.png', self.buyIn, 0, currentBet=None))
            else:
                return None
        else:
            print(self.playerNames)
            if len(self.players) <= 10 and name not in self.playerNames:
                self.players.append(Player(name, '../static/PNG-cards-1.3/None_of_None.png', '../static/PNG-cards-1.3/None_of_None.png', self.buyIn, 0))
            else:
                return None
    
    def isActive(self):
        return self.active
    
    def setBombPot(self):
        self.bombPot = True
    
    def activate(self):
        if len(self.players) >= 2:
            self.newRound()
            return "Activated!"
        return "Error: Not Enough Players."
    
    def json(self):
        try:
            game = deepcopy(self)
            game.setFlop1(game.getFlop1())
            game.setFlop2(game.getFlop2())
            game.setFlop3(game.getFlop3())
            game.setTurn(game.getTurn())
            game.setRiver(game.getRiver())
            game.setTableCards()
            for i in game.players:
                i.setCard1(i.getCard1())
                i.setCard2(i.getCard2())
            game.setPlayers([i.__dict__ for i in game.getPlayers()])
            return json.loads(json.dumps(game, default=lambda o: o.__dict__))
        except TypeError:
            game = deepcopy(self)
        
    
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
        