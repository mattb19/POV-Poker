class Card:
    def __init__(self, suit, num, value) -> None:
        self._suit = suit
        self._num = str(num)
        self._value = value
        self._id = [num, suit]
        
    def getSuit(self):
        return self._suit
    
    def getNum(self):
        return self._num
    
    def getValue(self):
        return self._value
    
    def getId(self):
        return self._id
    
    def __str__(self) -> str:
        return self._num+" of "+self._suit
    
    