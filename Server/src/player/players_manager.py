
class PlayersManager:
    def __init__(self, ws_server):
        self.ws_server = ws_server
        self.players = {}

    def handlePlayerLogin(self, msg, ws_addr):
        pass

    def handlePlayerLogout(self, msg, ws_addr):
        pass

    def handlePlayerOffline(self, playerId):
        pass

    def getPlayerById(self, playerId):
        if playerId in self.players:
            return self.players[playerId]
        return None

    def getPlayerByWsAddr(self, ws_addr):
        for id in self.players:
            if self.players[id].ws_addr == ws_addr:
                return self.players[id]
        return None

    def isPlayerOnline(self, playerId):
        return playerId in self.players

    