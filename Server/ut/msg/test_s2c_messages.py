import pytest
from msg.s2c_msgs import *


def test_s2c_msg():
    msg = S2CMsg(1)
    assert({"msgId": 1} == msg.serialize())
    with pytest.raises(Exception):
        msg.deserialize({"msgId": 20})

def test_dispatch_cards_ind():
    msg = DispatchCardsInd()
    data = {"msgId": OutMsgs.DISPATCH_CARDS_IND, "cards": [1, 2, 3], "roomId": 12, "playerId": 1}
    msg.deserialize(data)
    assert(msg.cards == data["cards"])
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(msg.playerId == data["playerId"])
    assert(data == msg.serialize())

def test_room_info_ind():
    msg = RoomInfoInd()
    data = {"msgId": OutMsgs.ROOM_INFO_IND, "roomId": 12, "playerId": 1}
    msg.deserialize(data)
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(msg.playerId == data["playerId"])
    assert(data == msg.serialize())

def test_game_start_ind():
    msg = GameStartInd()
    data = {"msgId": OutMsgs.GAME_START_IND, "roomId": 12}
    msg.deserialize(data)
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(data == msg.serialize())

def test_game_over_ind():
    msg = GameOverInd()
    data = {"msgId": OutMsgs.GAME_OVER_IND, "roomId": 12,
            "res": [{"playerId": 1, "score": 30, "cards": [1, 2, 3]}, {"playerId": 2, "score": 60, "cards": [5, 6]}]}
    msg.deserialize(data)
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    for i in range(len(data["res"])):
        assert(msg.res[i].playerId == data["res"][i]["playerId"])
        assert(msg.res[i].score == data["res"][i]["score"])
    assert(data == msg.serialize())

def test_player_deal_ind():
    msg = PlayerDealInd()
    data = {"msgId": OutMsgs.PLAYER_DEAL_IND, "cards": [1, 2, 3], "roomId": 12, "playerId": 1}
    msg.deserialize(data)
    assert(msg.cards == data["cards"])
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(msg.playerId == data["playerId"])
    assert(data == msg.serialize())

def test_player_pass_ind():
    msg = PlayerPassInd()
    data = {"msgId": OutMsgs.PLAYER_PASS_IND, "roomId": 12, "playerId": 1}
    msg.deserialize(data)
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(msg.playerId == data["playerId"])
    assert(data == msg.serialize())

def test_player_get_score_ind():
    msg = PlayerGetScoreInd()
    data = {"msgId": OutMsgs.PLAYER_GET_SCORE_IND, "roomId": 1, "playerId": 2, "scoreToAdd": 10, "scoreInTotal": 20}
    msg.deserialize(data)
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(msg.playerId == data["playerId"])
    assert(msg.scoreToAdd == data["scoreToAdd"])
    assert(msg.scoreInTotal == data["scoreInTotal"])
    assert(data == msg.serialize())

def test_player_join_room_ind():
    msg = PlayerJoinRoomInd()
    data = {"msgId": OutMsgs.PLAYER_JOIN_ROOM_IND, "roomId": 12, "playerId": 1}
    msg.deserialize(data)
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(msg.playerId == data["playerId"])
    assert(data == msg.serialize())

def test_player_leave_room_ind():
    msg = PlayerLeaveRoomInd()
    data = {"msgId": OutMsgs.PLAYER_LEAVE_ROOM_IND, "roomId": 12, "playerId": 1}
    msg.deserialize(data)
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(msg.playerId == data["playerId"])
    assert(data == msg.serialize())

def test_deal_owner_change_ind():
    msg = DealOwnerChangeInd()
    data = {"msgId": OutMsgs.DEAL_OWNER_CHANGE_IND, "roomId": 12, "playerId": 1}
    msg.deserialize(data)
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(msg.playerId == data["playerId"])
    assert(data == msg.serialize())

def test_player_ready_ind():
    msg = PlayerReadyInd()
    data = {"msgId": OutMsgs.PLAYER_READY_IND, "roomId": 12, "playerId": 1, "isReady": True}
    msg.deserialize(data)
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(msg.playerId == data["playerId"])
    assert(msg.isReady == data["isReady"])
    assert(data == msg.serialize())
