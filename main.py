from Card import Card
import random

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

for i in deck:
    print(i)
