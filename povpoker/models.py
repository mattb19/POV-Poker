from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    userID = Column(Integer,  primary_key=True, autoincrement=True)
    userName = Column(String(50), nullable=False)
    userEmail = Column(String(50), nullable=False)
    userPassword = Column(String(50), nullable=False)
    winCount = Column(Integer, default=0, nullable=False)
    straightCount = Column(Integer, default=0, nullable=False)
    flushCount = Column(Integer, default=0, nullable=False)
    fullHouseCount = Column(Integer, default=0, nullable=False)
    quadCount = Column(Integer, default=0, nullable=False)
    straightFlushCount = Column(Integer, default=0, nullable=False)
    royalFlushCount = Column(Integer, default=0, nullable=False)
    muckCount = Column(Integer, default=0, nullable=False)
    blind2Count = Column(Integer, default=0, nullable=False)
    blind4Count = Column(Integer, default=0, nullable=False)
    tenFlopCount = Column(Integer, default=0, nullable=False)
    tenCount = Column(Integer, default=0, nullable=False)
    tenPreFlopCount = Column(Integer, default=0, nullable=False)
    challengeCount = Column(Integer, default=0, nullable=False)
    challengeDenyCount = Column(Integer, default=0, nullable=False)
    flopPeekCount = Column(Integer, default=0, nullable=False)
    playerPeekCount = Column(Integer, default=0, nullable=False)