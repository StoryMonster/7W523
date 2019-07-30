from procedures.client_global_procedure import ClientGlobalProcedure
from procedures.client_events import *
import logging

class Client:
    def __init__(self, id, addr, server):
        self.id = id               # player id
        self.addr = addr           # websocket address
        self.server = server
        self.room_id = 0          # 0：未进入房间
        self.context = {"playerId": id, "addr": addr, "server": server, "roomId": self.room_id,
                        "isReady": False}
        self.procedure = ClientGlobalProcedure(self.context)

    def isRoomCorrect(self, roomId):
        return self.room_id == roomId

    def getWebSocketAddr(self):
        return self.addr

    def getId(self):
        return self.id

    def handle_login(self, msg):
        logging.debug(f"{self.id} is logged in")
        self.procedure.run()

    def handle_logout(self, msg):
        logging.debug(f"{self.id} is logged out")
        pass
    
    def handle_offline(self, msg):
        logging.debug(f"{self.id} offline")
        pass
    
    def enter_room(self, room_id, players_info):
        event = EnterRoomEvent({"roomId": room_id, "playersInfo": players_info})
        self.procedure.process_event(event)
    
    def handle_ready(self, msg):
        event = OnePlayerReadyEvent(msg["body"])
        self.procedure.process_event(event)

    def handle_not_ready(self, msg):
        event = OnePlayerNotReadyEvent(msg["body"])
        self.procedure.process_event(event)

    def handle_pass(self, msg):
        event = PassEvent(msg["body"])
        self.procedure.process_event(event)

    def handle_deal(self, msg):
        event = DealEvent(msg["body"])
        self.procedure.process_event(event)

    def handle_replay(self, msg):
        event = ReplayEvent(msg["body"])
        self.procedure.process_event(event)

    def game_over(self):
        event = GameOverEvent(msg["body"])
        self.procedure.process_event(event)
    
    def dispatch_cards(self, cards):
        event = DispatchCardsEvent({"cards": cards})
        self.procedure.process_event(event)

    def process_event(self, event):
        self.procedure.process_event(event)
