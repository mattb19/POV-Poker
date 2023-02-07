from Card import Card
import random
from Player import Player

class Game:
    def __init__(self, players, smallBlind, bigBlind) -> None:
        self.players = players
        self.deck = []
        self.pot = 0
        self.currentBet = 0
        self.round = 0
        self.currentPlayer = 0
        
        self.flop1 = None
        self.flop2 = None
        self.flop3 = None
        self.turn = None
        self.river = None
        
        self.smallBlind = smallBlind
        self.bigBlind = bigBlind
        
        self.shuffleDeck()
        self.dealCards()
    
    
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
        
        # rotates player list by 1
        for i in range(self.players):
            self.players = self.players[:1] + self.players[1:]
                
        # set everyones bet count to zero and turn to true
        self.players = [i.setCurrentBet(0) for i in self.players]
        self.players = [i.setTurn(True) for i in self.players]
        
        # set blinds bet count
        self.players[0].setCurrentBet(self.smallBlind)
        self.players[0].setChipCount(0-self.smallBlind)
        self.players[1].setCurrentBet(self.bigBlind)
        self.players[1].setChipCount(0-self.bigBlind)
        self.currentBet = self.bigBlind
        self.pot += self.bigBlind
        self.pot += self.smallBlind
        
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
        self.flop1 = tableCards[0]
        self.flop2 = tableCards[1]
        self.flop3 = tableCards[2]
        self.turn = tableCards[3]
        self.river = tableCards[4]
        
        # get player 3, set him to bet first
        self.currentPlayer = 2
    
    
    def placeBetFold(self, value):
        # get current player
        x = self.currentPlayer
        player = self.players[x]
        
        final = ""
        
        # if they fold
        if self.currentBet == None: 
            player.setFolded()
            player.setTurn(False)
            self.players[x] = player
            final = player.getUser().getUserName()+" Folds."
        
        # if they check
        elif value == 0 and player.getCurrentBet() == self.currentBet:
            player.setTurn(False)
            self.players[x] = player
            final = player.getUser().getUserName()+" Checks."
        
        # if they call
        elif value == self.currentBet and value < player.getChipCount(): 
            player.setCurrentBet(value)
            player.setChipCount(0-value)
            player.setTurn(False)
            self.pot += value
            self.players[x] = player
            final = player.getUser().getUserName()+" Calls "+str(value)+"!"
        
        # if they raise
        elif value >= self.currentBet and value < player.getChipCount():
            player.setCurrentBet(value)
            player.setChipCount(0-value)
            player.setTurn(False)
            self.currentBet = value
            self.pot += value
            self.players[x] = player
            final = player.getUser().getUserName()+" Bets "+str(value)+"!"
        
        # if they go all in
        elif value == player.getChipCount():
            player.setCurrentBet(value)
            player.setChipCount(0-value)
            player.setTurn(False)
            self.pot += value
            self.currentBet = value
            self.players[x] = player
            final = player.getUser().getUserName()+" IS ALL IN! "
        
        # if they don't bet enough
        elif value < self.currentBet:
            final = "You must put more in to call or raise"
        
        # if they put in too much
        elif value > player.getChipCount():
            final = "Insufficient Funds"
            
        # determine who goes next
        self.whoGoesNext()
        
        # set turn to true for all players who havent folded or called new bet
        for i in self.players:
            if i.getCurrentBet() == None:
                continue
            elif i.getCurrentBet() < value:
                i.setTurn(True)
        
        return final
        
    
    def revealCards(self):
        # set all players current bet count back to zero
        self.currentBet = 0
        self.players = [i.setCurrentBet(0) for i in self.players]
        
        
    def whoGoesNext(self): 
        # if its pre flop
        if self.round == 0:
            turns = [i.getTurn() for i in self.players]
            
            # if all players have called, checked or folded
            if True not in turns:
                self.currentPlayer = 0
                self.round += 1
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
                self.round += 1
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
                self.round += 1
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
                    
                
                
            
player = [Player(i,None,None,1000,0,i,0) for i in range(7)]
game = Game(player, 10, 12)