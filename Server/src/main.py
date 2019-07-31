from websocket_server import WebsocketServer
import logging

playersManager = None
msgReceiver = None
roomManager = None

def new_client_joint(client, server):
    logging.debug("new client connected")

def received_message(client, server, message):
    global msgReceiver
    if msgReceiver is not None:
        msgReceiver.onMsgReceived(client, message)

def client_leave(client, server):
    global playersManager, roomManager
    if playerManager is not None and roomManager is not None:
        player = playerManager.getPlayerByWsAddr(client)
        roomManager.handlePlayerOffline(player.playerId)
        playerManager.handlePlayerOffline(player.playerId)

if __name__ == "__main__":
    global playersManager, msgReceiver, roomManager
    server = WebsocketServer(host='127.0.0.1', port=12345)
    server.set_fn_new_client(new_client_joint)
    server.set_fn_message_received(received_message)
    server.set_fn_client_left(client_leave)
    server.run_forever()