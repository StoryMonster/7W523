import json


class Player:
    def __init__(self, playerId, ws_addr, ws_server):
        self.playerId = playerId
        self.ws_addr = ws_addr
        self.ws_server = ws_server
    
    def sendMsg(self, msg):
        self.ws_server.send_msg(self.ws_addr, json.dumps(msg))
