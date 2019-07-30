from websocket_server import WebsocketServer
import json
from clients.clients_manager import ClientsManager
from messages.message_handler_manager import MsgHandlerManager
import logging

msgHandlerManager = MsgHandlerManager()
clientsManager = ClientsManager(msgHandlerManager)

def new_client_joint(client, server):
    logging.debug("new client connected")

def received_message(client, server, message):
    global msgHandlerManager
    msgHandlerManager.receive(client, message)

def client_leave(client, server):
    global clientsManager
    clientsManager.handle_user_offline(client)


if __name__ == "__main__":
    server = WebsocketServer(host='127.0.0.1', port=12345)
    server.set_fn_new_client(new_client_joint)
    server.set_fn_message_received(received_message)
    server.set_fn_client_left(client_leave)
    clientsManager.set_websocket_server(server)
    server.run_forever()