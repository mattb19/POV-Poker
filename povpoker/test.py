from Game import Game
from Player import Player
import json
player = [Player("Jeremy",None,None,1000,0,0), Player("Matt",None,None,1000,1,0), Player("Trent",None,None,1000,2,0), Player("Ryan",None,None,1000,3,0), Player("Jackson",None,None,1000,4,0), Player("Luke",None,None,1000,5,0), Player("David",None,None,1000,6,0), Player("Max",None,None,1000,6,0), Player("Ethan",None,None,1000,6,0), Player("Jack",None,None,1000,6,0)]
game = Game(player, 10, 20, True)
game.newRound()
game.placeBetFold(20)
game.placeBetFold(20)
game.placeBetFold(20)
game.placeBetFold(20)
game.placeBetFold(20)
game.placeBetFold(20)
game.placeBetFold(20)
game.placeBetFold(20)
game.placeBetFold(10)
game.placeBetFold(0)

# game.setFlop1(game.getFlop1().__dict__)
# game.setFlop2(game.getFlop2().__dict__)
# game.setFlop3(game.getFlop3().__dict__)
# game.setTurn(game.getTurn().__dict__)
# game.setRiver(game.getRiver().__dict__)
# game.setTableCards()
# players = game.players
# for i in players:
#     i.setCard1(str(i.getCard1()))
#     i.setCard2(str(i.getCard2()))
# players = [i.__dict__ for i in players]
# game.setPlayers(players)



print(game.json())
