from .room import Room
from common.room_types import RoomType
from msg.in_msgs import InMsgs
import logging

class RoomManager:
### public
    def __init__(self, ws_server, playersMngr, msgReceiver):
        self.ws_server = ws_server
        self.playersMngr = playersMngr
        self.msgReceiver = msgReceiver
        self.rooms = {}
        self.maxRoomsSupport = 1000
        self.msgReceiver.register(InMsgs.PLAYER_ENTER_ROOM_IND, self.handlePlayerJoinRoom)
        self.msgReceiver.register(InMsgs.PLAYER_LEAVE_ROOM_IND, self.handlePlayerLeaveRoom)
        self.msgReceiver.register(InMsgs.PLAYER_READY_IND, self.handlePlayerReady)
        self.msgReceiver.register(InMsgs.PLAYER_PASS_IND, self.handlePlayerPass)
        self.msgReceiver.register(InMsgs.PLAYER_DEAL_IND, self.handlePlayerDeal)
        self.msgReceiver.register(InMsgs.PLAYER_DEAL_TIMEOUT_IND, self.handlePlayerDealTimeout)
    
    def handlePlayerJoinRoom(self, msg, ws_addr):
        room = self.selectValidRoom(msg.roomType)
        if room is None:
            room = self.createRoom(msg.roomType)
        player = self.playersMngr.getPlayerById(msg.playerId)
        room.hanldePlayerJoinRoom(player)

    def handlePlayerLeaveRoom(self, msg, ws_addr):
        room = self.getRoom(msg.roomId)
        if room is None:
            logging.error(f"The room {msg.roomId} is not exist")
            return
        player = self.playersMngr.getPlayerById(msg.playerId)
        room.handlePlayerLeaveRoom(player)
        if room.isEmpty():
            self.destroyRoom(room.roomId)

    def handlePlayerReady(self, msg, ws_addr):
        room = self.getRoom(msg.roomId)
        if room is None:
            logging.error(f"The room {msg.roomId} is not exist")
            return
        player = self.playersMngr.getPlayerById(msg.playerId)
        room.handlePlayerReady(player)

    def handlePlayerDeal(self, msg, ws_addr):
        room = self.getRoom(msg.roomId)
        if room is None:
            logging.error(f"The room {msg.roomId} is not exist")
            return
        player = self.playersMngr.getPlayerById(msg.playerId)
        room.handlePlayerDeal(player, msg.cards)

    def handlePlayerPass(self, msg, ws_addr):
        room = self.getRoom(msg.roomId)
        if room is None:
            logging.error(f"The room {msg.roomId} is not exist")
            return
        player = self.playersMngr.getPlayerById(msg.playerId)
        room.handlePlayerPass(player)

    def handlePlayerDealTimeout(self, msg, ws_addr):
        room = self.getRoom(msg.roomId)
        if room is None:
            logging.error(f"The room {msg.roomId} is not exist")
            return
        player = self.playersMngr.getPlayerById(msg.playerId)
        room.handlePlayerDealTimeout(player)
    
    def handlePlayerOffline(self, player):
        for id in self.rooms:
            if self.rooms[id].isPlayerInRoom(player.playerId):
                self.rooms[id].handlePlayerLeaveRoom(player)
                return
### private
    def generateRoomId(self):
        for i in range(1, self.maxRoomsSupport+1):
            if i not in self.rooms:
                return i
        logging.error("Max rooms reached")
        return None
    
    def createRoom(self, roomType):
        roomId = self.generateRoomId()
        if RoomType.TwoPlayersRoom == roomType:
            return Room(roomId, self.ws_server, 2)
        elif RoomType.ThreePlayersRoom == roomType:
            return Room(roomId, self.ws_server, 3)
        return None

    def destroyRoom(self, roomId):
        if roomId in self.rooms:
            del self.rooms[roomId]

    def getRoom(self, roomId):
        if roomId in self.rooms:
            return self.rooms[roomId]
        return None

    def selectValidRoom(self, roomType):
        for id in self.rooms:
            if self.rooms[id].roomType == roomType and not self.rooms[id].isFull():
                return self.rooms[id]

    