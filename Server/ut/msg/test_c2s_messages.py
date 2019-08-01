import pytest
from msg.c2s_msgs import *


def test_c2s_msg():
    msg = C2SMsg(0)
    data = {"msgId": 0, "playerId": 2}
    msg.deserialize(data)
    assert(msg.playerId == data["playerId"])
    assert(msg.msgId == data["msgId"])
    assert(data == msg.serialize())


def test_player_login_ind():
    msg = PlayerLoginInd()
    data = {"msgId": InMsgs.PLAYER_LOGIN_IND, "playerId": 2}
    msg.deserialize(data)
    assert(msg.playerId == data["playerId"])
    assert(msg.msgId == data["msgId"])
    assert(data == msg.serialize())

def test_player_logout_ind():
    msg = PlayerLogoutInd()
    data = {"msgId": InMsgs.PLAYER_LOGOUT_IND, "playerId": 2}
    msg.deserialize(data)
    assert(msg.playerId == data["playerId"])
    assert(msg.msgId == data["msgId"])
    assert(data == msg.serialize())

def test_player_enter_room_ind():
    msg = PlayerEnterRoomInd()
    data = {"msgId": InMsgs.PLAYER_ENTER_ROOM_IND, "playerId": 2, "roomType": RoomType.ThreePlayersRoom}
    msg.deserialize(data)
    assert(msg.playerId == data["playerId"])
    assert(msg.msgId == data["msgId"])
    assert(msg.roomType == data["roomType"])
    assert(data == msg.serialize())

def test_player_leave_room_ind():
    msg = PlayerLeaveRoomInd()
    data = {"msgId": InMsgs.PLAYER_LEAVE_ROOM_IND, "playerId": 2, "roomId": 12}
    msg.deserialize(data)
    assert(msg.playerId == data["playerId"])
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(data == msg.serialize())

def test_player_deal_timeout_ind():
    msg = PlayerDealTimeoutInd()
    data = {"msgId": InMsgs.PLAYER_DEAL_TIMEOUT_IND, "playerId": 2, "roomId": 23}
    msg.deserialize(data)
    assert(msg.playerId == data["playerId"])
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(data == msg.serialize())

def test_player_deal_ind():
    msg = PlayerDealInd()
    data = {"msgId": InMsgs.PLAYER_DEAL_IND, "playerId": 2, "roomId": 23, "cards": [1, 2, 3]}
    msg.deserialize(data)
    assert(msg.playerId == data["playerId"])
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(msg.cards == data["cards"])
    assert(data == msg.serialize())

def test_player_pass_ind():
    msg = PlayerPassInd()
    data = {"msgId": InMsgs.PLAYER_PASS_IND, "playerId": 2, "roomId": 23}
    msg.deserialize(data)
    assert(msg.playerId == data["playerId"])
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(data == msg.serialize())

def test_player_ready_ind():
    msg = PlayerReadyInd()
    data = {"msgId": InMsgs.PLAYER_READY_IND, "playerId": 2,  "roomId": 23, "isReady": True}
    msg.deserialize(data)
    assert(msg.playerId == data["playerId"])
    assert(msg.msgId == data["msgId"])
    assert(msg.roomId == data["roomId"])
    assert(msg.isReady == data["isReady"])
    assert(data == msg.serialize())