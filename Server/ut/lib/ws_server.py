

class WsServer:
    def __init__(self):
        self.latest_msg = None
        self.latest_client = None

    def send_msg(self, client, msg):
        client.put_message(msg)

    def put_message(self, client, msg):
        self.latest_client = client
        self.latest_msg = msg

    def receive(self):
        return self.latest_client, self.latest_msg

   