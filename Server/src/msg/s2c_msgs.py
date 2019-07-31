from out_msgs import OutMsgs
from collections import namedtuple

PlayerGameResult = namedtuple("PlayerGameResult", ["playerId", "cards", "score"])

class S2CMsg:
    def __init__(self, msgId=0):
        self.msgId = msgId

    def serialize(self):
        return {"msgId": self.msgId}

    def deserialize(self, data):
        self.msgId = data["msgId"]

class DispatchCardsInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.DISPATCH_CARDS_IND)
        self.playerId = 0
        self.cards = []
        self.roomId = 0

    def serialize(self):
        data = super().serialize()
        data["playerId"] = self.playerId
        data["cards"] = self.cards
        data["roomId"] = self.roomId
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.playerId = data["playerId"]
        self.cards = data["cards"]
        self.roomId = data["roomId"]

class GameOverInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.GAME_OVER_IND)
        self.roomId = 0
        self.res = []

    def serialize(self):
        data = super().serialize()
        data["roomId"] = self.roomId
        data["res"] = self.res
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.roomId = data["roomId"]
        self.res = data["res"]


class GameStartInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.GAME_START_IND)
        self.roomId = 0

    def serialize(self):
        data = super().serialize()
        data["roomId"] = self.roomId
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.roomId = data["roomId"]

class PlayerDealInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.PLAYER_DEAL_IND)
        self.playerId = 0
        self.roomId = 0
        self.cards = []

    def serialize(self):
        data = super().serialize()
        data["playerId"] = self.playerId
        data["roomId"] = self.roomId
        data["cards"] = self.cards
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.playerId = data["playerId"]
        self.roomId = data["roomId"]
        self.cards = data["cards"]


class PlayerPassInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.PLAYER_PASS_IND)
        self.roomId = 0
        self.playerId = 0

    def serialize(self):
        data = super().serialize()
        data["playerId"] = self.playerId
        data["roomId"] = self.roomId
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.playerId = data["playerId"]
        self.roomId = data["roomId"]

class PlayerGetScoreInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.PLAYER_GET_SCORE_IND)
        self.scoreToAdd = 0
        self.scoreInTotal = 0
        self.roomId = 0
        self.playerId = 0

    def serialize(self):
        data = super().serialize()
        data["scoreToAdd"] = self.scoreToAdd
        data["scoreInTotal"] = self.scoreInTotal
        data["roomId"] = self.roomId
        data["playerId"] = self.playerId
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.playerId = data["playerId"]
        self.roomId = data["roomId"]
        self.scoreToAdd = data["scoreToAdd"]
        self.scoreInTotal = data["scoreInTotal"]

class PlayerShowCardsInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.PLAYER_SHOW_CARDS_IND)
        self.playerId = 0
        self.roomId = 0
        self.cards = []

    def serialize(self):
        data = super().serialize()
        data["playerId"] = self.playerId
        data["roomId"] = self.roomId
        data["cards"] = self.cards
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.playerId = data["playerId"]
        self.roomId = data["roomId"]
        self.cards = data["cards"]

class RoomInfoInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.ROOM_INFO_IND)
        self.roomId = 0
        self.playerId = 0

    def serialize(self):
        data = super().serialize()
        data["roomId"] = self.roomId
        data["playerId"] = self.playerId
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.roomId = data["roomId"]
        self.playerId = data["playerId"]

class PlayerJoinRoomInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.PLAYER_JOIN_ROOM_IND)
        self.roomId = 0
        self.playerId = 0

    def serialize(self):
        data = super().serialize()
        data["roomId"] = self.roomId
        data["playerId"] = self.playerId
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.playerId = data["playerId"]
        self.roomId = data["roomId"]

class PlayerLeaveRoomInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.PLAYER_LEAVE_ROOM_IND)
        self.roomId = 0
        self.playerId = 0

    def serialize(self):
        data = super().serialize()
        data["roomId"] = self.roomId
        data["playerId"] = self.playerId
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.playerId = data["playerId"]
        self.roomId = data["roomId"]

class PlayerReadyInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.PLAYER_READY_IND)
        self.roomId = 0
        self.playerId = 0
        self.isReady = False

    def serialize(self):
        data = super().serialize()
        data["roomId"] = self.roomId
        data["playerId"] = self.playerId
        data["isReady"] = self.isReady
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.playerId = data["playerId"]
        self.roomId = data["roomId"]
        self.isReady = data["isReady"]

class DealOwnerChangeInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.DEAL_OWNER_CHNAGE_IND)
        self.playerId = 0
        self.roomId = 0

    def serialize(self):
        data = super().serialize()
        data["playerId"] = self.playerId
        data["roomId"] = self.roomId
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.playerId = data["playerId"]
        self.roomId = data["roomId"]