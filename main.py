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
        for i in self.players:
            i.setCurrentBet(0)
        for i in self.players:
            i.setTurn(True)
        
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
                for i in self.players:
                    if i.getCurrentBet is not None:
                        i.setCurrentBet(0)
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
                for i in self.players:
                    if i.getCurrentBet is not None:
                        i.setCurrentBet(0)
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
                for i in self.players:
                    if i.getCurrentBet is not None:
                        i.setCurrentBet(0)
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
                    if i.getCurrentBet is not None:
                        i.setCurrentBet(0)
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
            unsortedCards = [[i.getNum(), i.getSuit()] for i in lst]
            card = sorted(unsortedCards,key=lambda l:l[0])
            cards = [i[0] for i in card]
            suits = [i[1] for i in card]
            
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
            
            
            pair1 = 0
            pair2 = 0
            card5 = 0
            twoPair = []
            for j in cards:
                if cards.count(j) == 2 and j > pair1 and j != pair2:
                    pair1 = j
                elif cards.count(j) == 2 and j > pair2 and j != pair1:
                    pair2 = j
            if pair1 != 0 and pair2 != 0 and len(twoPair) != 0:
                twoPair.append(pair1)
                twoPair.append(pair2)
                twoPair.sort()
                newCards = [i for i in cards if i != pair1 or i != pair2]
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
                
                i.setCurrentBet(10000)
            
            # straight flush check
            elif ((cards[0]+1 == cards[1] and cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and 
                suits[0] == suits[1] and suits[1] == suits[2] and suits[2] == suits[3] and suits[3] == suits[4]) or
                (cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5] and 
                suits[1] == suits[2] and suits[2] == suits[3] and suits[3] == suits[4] and suits[4] == suits[5]) or
                (cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5] and cards[5]+1 == cards[6] and 
                suits[2] == suits[3] and suits[3] == suits[4] and suits[4] == suits[5] and suits[5] == suits[6])):
                
                if cards[4]-cards[0] == 4:
                    x = 9000+cards[4]+cards[3]+cards[2]+cards[1]+cards[0]
                    i.setCurrentBet(x)
                elif cards[5]-cards[1] == 4:
                    x = 9000+cards[5]+cards[4]+cards[3]+cards[2]+cards[1]
                    i.setCurrentBet(x)
                elif cards[6]-cards[2] == 4:
                    x = 9000+cards[6]+cards[5]+cards[4]+cards[3]+cards[2]
                    i.setCurrentBet(x)

            # quads check
            elif quads != 0:
                x = 8000+(quads*4)
                i.setCurrentBet(x)
            
            # full house check
            elif len(fullHouse) != 0:
                x = 7000+(fullHouse[0]*30)+(fullHouse[1]*2)
                i.setCurrentBet(x)
            
            # flush check
            elif suits.count("Hearts") == 5 or suits.count("Spades") == 5 or suits.count("Diamonds") == 5 or suits.count("Clubs") == 5:
                x = 0
                if suits.count("Hearts") == 5:
                    flush = [i for i in card if i[1] == "Hearts"]
                    flushCount = [i[0] for i in flush]
                    x = 6000+max(flushCount)
                elif suits.count("Spades") == 5:
                    flush = [i for i in card if i[1] == "Spades"]
                    flushCount = [i[0] for i in flush]
                    x = 6000+max(flushCount)
                elif suits.count("Diamonds") == 5:
                    flush = [i for i in card if i[1] == "Diamonds"]
                    flushCount = [i[0] for i in flush]
                    x = 6000+max(flushCount)
                elif suits.count("Clubs") == 5:
                    flush = [i for i in card if i[1] == "Clubs"]
                    flushCount = [i[0] for i in flush]
                    x = 6000+max(flushCount)
                i.setCurrentBet(x)
            
            # straight check
            elif ((cards[0]+1 == cards[1] and cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4]) or
                (cards[1]+1 == cards[2] and cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5]) or
                (cards[2]+1 == cards[3] and cards[3]+1 == cards[4] and cards[4]+1 == cards[5] and cards[5]+1 == cards[6])):
                if cards[4]-cards[0] == 4:
                    x = 5000+cards[4]+cards[3]+cards[2]+cards[1]+cards[0]
                    i.setCurrentBet(x)
                elif cards[5]-cards[1] == 4:
                    x = 5000+cards[5]+cards[4]+cards[3]+cards[2]+cards[1]
                    i.setCurrentBet(x)
                elif cards[6]-cards[2] == 4:
                    x = 5000+cards[6]+cards[5]+cards[4]+cards[3]+cards[2]
                    i.setCurrentBet(x)
            
            # trips check
            elif trips != 0:
                x = 4000 + (trips*30) + one + two
                i.setCurrentBet(x)
            
            # two pair check
            elif len(twoPair) != 0:
                x = 3000 + (twoPair[0]*2) + (twoPair[1]*20) + card5
                i.setCurrentBet(x)
            
            # pair check
            elif pair != 0:
                x = 2000 + pair*40 + otherCards[0]*15 + otherCards[1]*10 + otherCards[2]*5
                i.setCurrentBet(x)
                
            # high card check
            else:
                x = highCards[0]*50 + highCards[1]*40 + highCards[2]*30 + highCards[3]*20 + highCards[4]*10
                i.setCurrentBet(x)
        
        
        # check who won the hand
        winner = []
        high = 0
        for i in finalPlayers:
            if i.getCurrentBet() > high:
                if len(winner) != 0:
                    winner.clear()
                winner.append(i)
            if i.getCurrentBet() == high:
                winner.append(i)
        winners = []
        for i in winner:
            winners.append([i, i.getCurrentBet()])
        return winners
            
                
            
                
                    
                
                
            
player = [Player(i,None,None,1000,0,i,0) for i in range(7)]
game = Game(player, 10, 12)