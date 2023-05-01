from Game import Game
from Player import Player
import json
player = [Player("Matt",None,None,1000,0), Player("Trent",None,None,1000,0), Player("Jack",None,None,1000,0), Player("Jeremy",None,None,1000,0), Player("Jackson",None,None,1000,0), Player("David",None,None,1000,0)]
game = Game(1, player, 10, 20)
data = game.json()
x = Game(**data)
print(x._players)

