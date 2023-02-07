from Card import Card
import random
from Player import Player

class Game:
    def __init__(self, players, smallBlind, bigBlind) -> None:
        self.players = players
        self.deck = []
        self.pot = 0
        self.flop = None
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
        # generates a new deck
        self.shuffleDeck()
        
        # rotates player list based on who are blinds
        for i in range(self.players):
            if self.players[i].getBlind() == 'small':
                self.players = self.players[:i] + self.players[i:]
        
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
        self.flop = tableCards[:3]
        self.turn = tableCards[3]
        self.river = tableCards[4]