from .out_msgs import OutMsgs
from collections import namedtuple

PlayerGameResult = namedtuple("PlayerGameResult", ["playerId", "cards", "score"])
PublicPlayerInfoInRoom = namedtuple("PublicPlayerInfoInRoom", ["playerId", "roomId", "index", "isReady"])


class S2CMsg:
    def __init__(self, msgId=0):
        self.msgId = msgId

    def serialize(self):
        return {"msgId": self.msgId}

    def deserialize(self, data):
        assert(self.msgId == data["msgId"])

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
        data["res"] = []
        for elem in self.res:
            data["res"].append({"playerId": elem.playerId, "cards": elem.cards, "score": elem.score})
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.roomId = data["roomId"]
        self.res = []
        for elem in data["res"]:
            self.res.append(PlayerGameResult(elem["playerId"], elem["cards"], elem["score"]))

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

class RoomInfoInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.ROOM_INFO_IND)
        self.players = []

    def serialize(self):
        data = super().serialize()
        data["players"] = []
        for player in self.players:
            data["players"].append({"playerId": player.playerId, "roomId": player.roomId, "index": player.index, "isReady": player.isReady})
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.players = []
        for player in data["players"]:
            self.players.append(PublicPlayerInfoInRoom(player["playerId"], player["roomId"], player["index"], player["isReady"]))

class PlayerJoinRoomInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.PLAYER_JOIN_ROOM_IND)
        self.playerInfo = PublicPlayerInfoInRoom(0, 0, 0, False)

    def serialize(self):
        data = super().serialize()
        data["playerInfo"] = {}
        data["playerInfo"]["roomId"] = self.playerInfo.roomId
        data["playerInfo"]["playerId"] = self.playerInfo.playerId
        data["playerInfo"]["index"] = self.playerInfo.index
        data["playerInfo"]["isReady"] = self.playerInfo.isReady
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.playerInfo = PublicPlayerInfoInRoom(data["playerInfo"]["playerId"], data["playerInfo"]["roomId"], data["playerInfo"]["index"], data["playerInfo"]["isReady"])

class PlayerLeaveRoomInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.PLAYER_LEAVE_ROOM_IND)
        self.playerInfo = PublicPlayerInfoInRoom(0, 0, 0, False)

    def serialize(self):
        data = super().serialize()
        data["playerInfo"] = {}
        data["playerInfo"]["roomId"] = self.playerInfo.roomId
        data["playerInfo"]["playerId"] = self.playerInfo.playerId
        data["playerInfo"]["index"] = self.playerInfo.index
        data["playerInfo"]["isReady"] = self.playerInfo.isReady
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.playerInfo = PublicPlayerInfoInRoom(data["playerInfo"]["playerId"], data["playerInfo"]["roomId"], data["playerInfo"]["index"], data["playerInfo"]["isReady"])

class PlayerReadyInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.PLAYER_READY_IND)
        self.playerInfo = PublicPlayerInfoInRoom(0, 0, 0, False)

    def serialize(self):
        data = super().serialize()
        data["playerInfo"] = {}
        data["playerInfo"]["roomId"] = self.playerInfo.roomId
        data["playerInfo"]["playerId"] = self.playerInfo.playerId
        data["playerInfo"]["index"] = self.playerInfo.index
        data["playerInfo"]["isReady"] = self.playerInfo.isReady
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.playerInfo = PublicPlayerInfoInRoom(data["playerInfo"]["playerId"], data["playerInfo"]["roomId"], data["playerInfo"]["index"], data["playerInfo"]["isReady"])

class DealOwnerChangeInd(S2CMsg):
    def __init__(self):
        super().__init__(OutMsgs.DEAL_OWNER_CHANGE_IND)
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