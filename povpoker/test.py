from Game import Game
from Player import Player
import json
player = [Player("Matt",None,None,1000,0), Player("Trent",None,None,1000,0), Player("Jack",None,None,1000,0), Player("Jeremy",None,None,1000,0), Player("Jackson",None,None,1000,0), Player("David",None,None,1000,0)]
game = Game(1, player, 10, 20)
game.newRound()
game.placeBetFold(20)
game.placeBetFold(20)
game.placeBetFold(20)
game.placeBetFold(20)
game.placeBetFold(20)
game.placeBetFold(20)


data = game.json()

datas = str(data)
datas = eval(datas)



players = [Player(**i) for i in data["players"]]


cardVals = {"2" : 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7, "8" : 8, "9" : 9, "10" : 10, "jack" : 11, "queen" : 12, "king" : 13, "ace" : 14}



del data["players"]

    
x = Game(**data, players=players)


str = "../static/PNG-cards-1.3/10_of_Spades.png"
str = str[24:-4]
str = str.split("_")
str.pop(1)
str[0] = int(str[0])
print(str)
