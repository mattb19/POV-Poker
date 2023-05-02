class Card:
    def __init__(self, _suit, _num, _value) -> None:
        self._suit = _suit
        self._num = str(_num)
        self._value = _value
        
    def getSuit(self):
        return self._suit
    
    def getNum(self):
        return self._num
    
    def getValue(self):
        return self._value
    
    def getId(self):
        return [self._num, self._suit]
    
    def __str__(self) -> str:
        '''gfgg'''
        cee = {
            "3" : "three",
            "2" : "two",
            "4" : "four",
            "5" : "five",
            "6" : "six",
            "7" : "seven",
            "8" : "eight",
            "9" : "nine",
            "10" : "ten",
            "Ace" : "ace",
            "King" : "king",
            "Queen" : "queen",
            "Jack" : "jack",
        }
        return "../static/PNG-cards-1.3/"+self._num+"_of_"+self._suit+".png"

    