from Card import Card
import random
from Player import Player

players = []

def shuffleDeck():
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
    numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    deck = []
    for i, suit in enumerate(suits):
        for j, num in enumerate(numbers):
            deck.append(Card(suit, num, values[j]))

    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)

    return deck

def dealCards(players, deck):
    for i in range(1, len(players)):
        players[i].setCard1(deck[-1])
        deck.pop()
    for i in range(1, len(players)):
        players[i].setCard2(deck[-1])
        deck.pop()
    return [deck, players]