from .in_msgs import InMsgs
from common.room_types import RoomType

class C2SMsg:
    def __init__(self, msgId=0):
        self.msgId = msgId
        self.playerId = 0
    
    def serialize(self):
        data = {}
        data["msgId"] = self.msgId
        data["playerId"] = self.playerId
        return data

    def deserialize(self, data):
        assert(self.msgId == data["msgId"])
        self.playerId = data["playerId"]

class PlayerLoginInd(C2SMsg):
    def __init__(self):
        super().__init__(InMsgs.PLAYER_LOGIN_IND)

class PlayerLogoutInd(C2SMsg):
    def __init__(self):
        super().__init__(InMsgs.PLAYER_LOGOUT_IND)

class PlayerEnterRoomInd(C2SMsg):
    def __init__(self):
        super().__init__(InMsgs.PLAYER_ENTER_ROOM_IND)
        self.roomType = RoomType.TwoPlayersRoom

    def serialize(self):
        data = super().serialize()
        data["roomType"] = self.roomType
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.roomType = RoomType(data["roomType"])

class PlayerLeaveRoomInd(C2SMsg):
    def __init__(self):
        super().__init__(InMsgs.PLAYER_LEAVE_ROOM_IND)
        self.roomId = 0

    def serialize(self):
        data = super().serialize()
        data["roomId"] = self.roomId
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.roomId = data["roomId"]

class PlayerReadyInd(C2SMsg):
    def __init__(self):
        super().__init__(InMsgs.PLAYER_READY_IND)
        self.isReady = False
        self.roomId = 0

    def serialize(self):
        data = super().serialize()
        data["roomId"] = self.roomId
        data["isReady"] = self.isReady
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.roomId = data["roomId"]
        self.isReady = data["isReady"]

class PlayerPassInd(C2SMsg):
    def __init__(self):
        super().__init__(InMsgs.PLAYER_PASS_IND)
        self.roomId = 0

    def serialize(self):
        data = super().serialize()
        data["roomId"] = self.roomId
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.roomId = data["roomId"]

class PlayerDealInd(C2SMsg):
    def __init__(self):
        super().__init__(InMsgs.PLAYER_DEAL_IND)
        self.roomId = 0
        self.cards = []

    def serialize(self):
        data = super().serialize()
        data["roomId"] = self.roomId
        data["cards"] = self.cards
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.roomId = data["roomId"]
        self.cards = data["cards"]

class PlayerDealTimeoutInd(C2SMsg):
    def __init__(self):
        super().__init__(InMsgs.PLAYER_DEAL_TIMEOUT_IND)
        self.roomId = 0

    def serialize(self):
        data = super().serialize()
        data["roomId"] = self.roomId
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.roomId = data["roomId"]
