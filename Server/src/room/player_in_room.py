
class PlayerInRoom:
    def __init__(self, player, index):
        self.player = player
        self.index = index
        self.cards = []
        self.isReady = False
        self.isPassing = False
        self.score = 0

    def getId(self):
        return self.player.playerId

    def sendMsg(self, msg):
        self.player.sendMsg(msg)
