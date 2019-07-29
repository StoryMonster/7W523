from .client import Client
from messages.out_msgs import OutMsgs
from messages.in_msgs import InMsgs
import logging
import json

class ClientsManager:
    def __init__(self, msgHandlerManager):
        self.clients = {}
        self.websocket_server = None
        self.msgHandlerManager = msgHandlerManager
        self.msgHandlerManager.register(InMsgs.CLIENT_LOGIN_IND, self.userLogin)
        self.msgHandlerManager.register(InMsgs.CLIENT_LEAVE_IND, self.userLogout)
        self.msgHandlerManager.register(InMsgs.CLIENT_CHOOSE_ROOM_IND, self.userChoosedRoom)
        self.msgHandlerManager.register(InMsgs.CLIENT_READY_IND, self.userReady)
        self.msgHandlerManager.register(InMsgs.CLIENT_NOT_READY_IND, self.userNotReady)

    def __del__(self):
        self.msgHandlerManager.deregister(InMsgs.CLIENT_LOGIN_IND)
        self.msgHandlerManager.deregister(InMsgs.CLIENT_LEAVE_IND)
        self.msgHandlerManager.deregister(InMsgs.CLIENT_CHOOSE_ROOM_IND)
        self.msgHandlerManager.deregister(InMsgs.CLIENT_READY_IND)
        self.msgHandlerManager.deregister(InMsgs.CLIENT_NOT_READY_IND)

    def set_websocket_server(self, server):
        self.websocket_server = server

    def sendMessageToPlayerById(self, playerId, msgId, msg):
        if self.websocket_server is None or playerId not in self.clients: return
        addr = self.clients[playerId].getWebSocketAddr()
        header = {"msgId": msgId, "playerId": playerId}
        data = json.dumps({"header": header, "body": msg})
        self.websocket_server.send_message(addr, data)

    def broadcast(self, msgId, msg):
        if self.websocket_server is None: return
        header = {"msgId": msgId, "playerId": "_"}
        data = json.dumps({"header": header, "body": msg})
        self.websocket_server.send_message_to_all(data)

    def userLogin(self, addr, msg):
        playerId = msg["header"]["playerId"]
        logging.debug(f"Player {playerId} login")
        if playerId in self.clients:
            logging.error(f"{playerId} is already in game!!")
            return
        self.clients[playerId] = Client(playerId, addr)

    def userLogout(self, addr, msg):
        playerId = msg["header"]["playerId"]
        logging.debug(f"Player {playerId} logout")
        if playerId not in self.clients:
            logging.error(f"{playerId} is not in game, so he/she should have already left the game")
            return
        del self.clients[playerId]

    def userOffline(self, addr):
        for id in self.clients:
            if addr == self.clients[id].getWebSocketAddr():
                logging.info(f"{self.clients[id].getId()} offline")
                del self.clients[id]
                return

    def userChoosedRoom(self, addr, msg):
        playerId = msg["header"]["playerId"]
        logging.debug(f"Player {playerId} choosed room")

    def userReady(self, addr, msg):
        playerId = msg["header"]["playerId"]
        logging.debug(f"Player {playerId} ready")
        self.sendMessageToPlayerById(playerId, OutMsgs.GAME_START_IND, {})
        self.sendMessageToPlayerById(playerId, OutMsgs.CARDS_DISPATCH_IND, {"cardIds": [1, 2, 3, 4, 5]})

    def userNotReady(self, addr, msg):
        playerId = msg["header"]["playerId"]
        logging.debug(f"Player {playerId} not ready")