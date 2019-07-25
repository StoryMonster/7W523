from .client import Client
from websocket_server import WebsocketServer

class ClientsManager(WebsocketServer):
    def __init__(self, host='127.0.0.1', port=12345):
        super().__init__(host=host, port=port)
        self.set_fn_new_client(self.new_client_joint)
        self.set_fn_message_received(self.received_message)
        self.set_fn_client_left(self.client_leave)
        self.clientsContainer = {}          # id:Client   websocket_server中已有定义clients，故而取了一个很差的名字

    def new_client_joint(self, client, server):
        print("new client connected")

    def received_message(self, client, server, message):
        print("received message")

    def client_leave(self, client, server):
        print("client left")

    def sendMessageToClientById(self, clientId, msg):
        if clientId not in self.clientsContainer: return
        addr = self.clientsContainer[clientId].getWebSocketAddr()
        if addr in self.clients:
            self.send_message(addr, msg)

    def broadcast(self, msg):
        self.send_message_to_all(msg)