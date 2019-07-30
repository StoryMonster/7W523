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
        self.msgHandlerManager.register(InMsgs.CLIENT_LOGIN_IND, self.handle_user_login)
        self.msgHandlerManager.register(InMsgs.CLIENT_LEAVE_IND, self.handle_user_logout)
        self.msgHandlerManager.register(InMsgs.CLIENT_CHOOSE_ROOM_IND, self.handle_user_enter_room)
        self.msgHandlerManager.register(InMsgs.CLIENT_READY_IND, self.handle_user_ready)
        self.msgHandlerManager.register(InMsgs.CLIENT_NOT_READY_IND, self.handle_user_not_ready)
        self.msgHandlerManager.register(InMsgs.CLIENT_PASS_IND, self.handle_user_pass)
        self.msgHandlerManager.register(InMsgs.CLIENT_DEAL_IND, self.handle_user_deal)

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

    def handle_user_login(self, addr, msg):
        playerId = msg["header"]["playerId"]
        if playerId in self.clients:
            logging.error(f"{playerId} is already in game!!")
            return
        self.clients[playerId] = Client(playerId, addr, self.websocket_server)
        self.clients[playerId].handle_login(msg)

    def handle_user_logout(self, addr, msg):
        playerId = msg["header"]["playerId"]
        logging.debug(f"Player {playerId} logout")
        if playerId not in self.clients:
            logging.error(f"{playerId} is not in game, so he/she should have already left the game")
            return
        del self.clients[playerId]

    def handle_user_offline(self, addr):
        for id in self.clients:
            if addr == self.clients[id].getWebSocketAddr():
                logging.info(f"{self.clients[id].getId()} offline")
                del self.clients[id]
                return

    def handle_user_enter_room(self, addr, msg):
        playerId = msg["header"]["playerId"]
        logging.debug(f"Player {playerId} choosed room")

    def handle_user_ready(self, addr, msg):
        playerId = msg["header"]["playerId"]
        logging.debug(f"Player {playerId} ready")
        self.sendMessageToPlayerById(playerId, OutMsgs.GAME_START_IND, {})
        self.sendMessageToPlayerById(playerId, OutMsgs.CARDS_DISPATCH_IND, {"cardIds": [1, 2, 3, 4, 5]})

    def handle_user_not_ready(self, addr, msg):
        playerId = msg["header"]["playerId"]
        logging.debug(f"Player {playerId} not ready")
    
    def handle_user_pass(self, addr, msg):
        playerId = msg["header"]["playerId"]
        logging.debug(f"Player {playerId} pass")

    def handle_user_deal(self, addr, msg):
        playerId = msg["header"]["playerId"]
        logging.debug(f"Player {playerId} deal")