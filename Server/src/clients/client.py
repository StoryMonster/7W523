

class Client:
    def __init__(self, id, addr):
        self.id = id               # player id
        self.addr = addr           # websocket address

    def getWebSocketAddr(self):
        return self.addr

    def getId(self):
        return self.id
