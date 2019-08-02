import json
import queue

class WsClient:
    def __init__(self):
        self.server = None
        self.received_msgs = queue.Queue()

    def connect(self, server):
        self.server = server

    def send_message(self, msg):
        if self.server is not None:
            self.server.put_message(self, msg)

    def put_message(self, msg):
        self.received_msgs.put_nowait(msg)

    def receive(self):
        msg = self.received_msgs.get_nowait()
        return json.loads(msg)

    def latest_receive(self):
        last_msg = None
        while not self.received_msgs.empty():
            last_msg = self.received_msgs.get_nowait()
        return json.loads(last_msg)
