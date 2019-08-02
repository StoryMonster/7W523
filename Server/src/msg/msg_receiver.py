from .c2s_msg_container import C2SMsgContainer
import logging
import json

class MsgReceiver:
    def __init__(self):
        self.c2sMsgContainer = C2SMsgContainer()
        self.msgHandlers = {}

    def register(self, msgId, handler):
        if msgId in self.msgHandlers:
            logging.error(f"message {msgId} is already registerred")
            return
        self.msgHandlers[msgId] = handler

    def deregister(self, msgId):
        if msgId not in self.msgHandlers:
            logging.error(f"message {msgId} is not registerred")
            return
        del self.msgHandlers[msgId]

    def onMsgReceived(self, ws_addr, data):
        serialized = json.loads(data)
        msg = self.c2sMsgContainer.getTemplate(serialized["msgId"])()
        if msg is None:
            logging.error(f"Unknown msg: {serialized}")
            return
        msg.deserialize(serialized)
        handler = self.getHandler(msg.msgId)
        if handler is None:
            logging.error(f"No handler for msg {msg.msgId}")
            return
        handler(msg, ws_addr)
    
    def getHandler(self, msgId):
        if msgId in self.msgHandlers:
            return self.msgHandlers[msgId]
        return None


