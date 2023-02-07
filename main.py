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
                
        # set everyones bet count to zero
        self.players = [i.setCurrentBet(0) for i in self.players]
        
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
            player.setCurrentBet(None)
            self.players[x] = player
            final = player.getUser().getUserName()+" Folds."
        
        # if they call
        elif value == self.currentBet and value < player.getChipCount(): 
            player.setCurrentBet(value)
            player.setChipCount(0-value)
            self.pot += value
            self.players[x] = player
            final = player.getUser().getUserName()+" Calls "+str(value)+"!"
        
        # if they raise
        elif value >= self.currentBet and value < player.getChipCount():
            player.setCurrentBet(value)
            player.setChipCount(0-value)
            self.currentBet = value
            self.pot += value
            self.players[x] = player
            final = player.getUser().getUserName()+" Bets "+str(value)+"!"
        
        # if they go all in
        elif value == player.getChipCount():
            player.setCurrentBet(value)
            player.setChipCount(0-value)
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
        
        return final
        
    
    def revealCards(self):
        # set all players current bet count back to zero
        self.currentBet = 0
        self.players = [i.setCurrentBet(0) for i in self.players]
        
        
    def whoGoesNext(self): 
        