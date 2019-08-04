from websocket_server import WebsocketServer
from msg.msg_receiver import MsgReceiver
from player.players_manager import PlayersManager
from room.rooms_manager import RoomManager
import logging

global playersManager
global msgReceiver
global roomManager

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='../server_running.log',
                    filemode='w')


def new_client_joint(client, server):
    logging.debug("new client connected")
    print("new client connected")

def received_message(client, server, message):
    global msgReceiver
    if msgReceiver is not None:
        msgReceiver.onMsgReceived(client, message)

def client_leave(client, server):
    global playersManager, roomManager
    if playersManager is not None and roomManager is not None:
        player = playersManager.getPlayerByWsAddr(client)
        if player is not None:
            roomManager.handlePlayerOffline(player)
            playersManager.handlePlayerOffline(player.playerId)

if __name__ == "__main__":
    server = WebsocketServer(host='192.168.1.100', port=12345)
    server.set_fn_new_client(new_client_joint)
    server.set_fn_message_received(received_message)
    server.set_fn_client_left(client_leave)
    global playersManager, msgReceiver, roomManager
    msgReceiver = MsgReceiver()
    playersManager = PlayersManager(server, msgReceiver)
    roomManager = RoomManager(server, playersManager, msgReceiver)
    server.run_forever()
