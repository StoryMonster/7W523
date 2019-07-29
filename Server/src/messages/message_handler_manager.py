import logging
import json
from .in_msgs import InMsgs
from .out_msgs import OutMsgs

class MsgHandlerManager:
    def __init__(self):
        self.msgHandlers = {}

    def register(self, msgId, msgHandler):
        if msgId not in self.msgHandlers:
            self.msgHandlers[msgId] = msgHandler
            return
        logging.warn(f"{msgId} was registered")

    def deregister(self, msgId):
        if msgId not in self.msgHandlers:
            logging.warn(f"{msgId} cannot be deregistered, since no handler is found bind for it")
            return
        del self.msgHandlers[msgId]
        logging.info(f"{msgId} is deregistered")

    def getHandler(self, msgId):
        return self.msgHandlers[msgId] if msgId in self.msgHandlers else None

    def receive(self, addr, data):
        msg = json.loads(data)
        header = msg["header"]
        #body = msg["body"]
        msgId = header["msgId"]
        handler = self.getHandler(msgId)
        if handler is None:
            logging.warn(f"Cannot find handler for message {msgId}")
            return
        handler(addr, msg)
