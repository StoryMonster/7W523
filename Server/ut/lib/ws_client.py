

class WsClient:
    def __init__(self):
        self.server = None
        self.latest_msg = None

    def connect(self, server):
        self.server = server

    def send_message(self, msg):
        if self.server is not None:
            self.server.put_message(self, msg)

    def put_message(self, msg):
        self.latest_msg = msg

    def receive(self):
        return self.latest_msg
