import logging
from .player import Player
from msg.in_msgs import InMsgs

class PlayersManager:
    def __init__(self, ws_server, msgReceivers):
        self.ws_server = ws_server
        self.players = {}
        self.msgReceivers = msgReceivers
        self.msgReceivers.register(InMsgs.PLAYER_LOGIN_IND, self.handlePlayerLogin)
        self.msgReceivers.register(InMsgs.PLAYER_LOGOUT_IND, self.handlePlayerLogout)

    def handlePlayerLogin(self, msg, ws_addr):
        if self.isPlayerOnline(msg.playerId):
            logging.error(f"player {msg.playerId} is already on line")
            return
        self.players[msg.playerId] = Player(msg.playerId, ws_addr, self.ws_server)
        logging.info(f"player {msg.playerId} login")

    def handlePlayerLogout(self, msg, ws_addr):
        if not self.isPlayerOnline(msg.playerId):
            logging.error(f"player {msg.playerId} is not on line")
            return
        del self.players[msg.playerId]
        logging.info(f"player {msg.playerId} logout")

    def handlePlayerOffline(self, playerId):
        if not self.isPlayerOnline(playerId):
            logging.error(f"player {playerId} is not on line")
            return
        del self.players[playerId]
        logging.info(f"player {playerId} offline")

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

    