import pytest
import json
from msg.msg_receiver import MsgReceiver
from msg.in_msgs import InMsgs
from msg.c2s_msgs import PlayerLoginInd, PlayerLogoutInd

def test_on_received_msg():
    msgReceiver = MsgReceiver()
    players = []
    def callback_add(msg, ws_addr):
        assert(msg.msgId == InMsgs.PLAYER_LOGIN_IND)
        players.append(1)
    def callback_decrese(msg, ws_addr):
        assert(msg.msgId == InMsgs.PLAYER_LOGOUT_IND)
        del players[0]
    msgReceiver.register(InMsgs.PLAYER_LOGIN_IND, callback_add)
    msgReceiver.register(InMsgs.PLAYER_LOGOUT_IND, callback_decrese)
    loginMsg = PlayerLoginInd()
    loginMsg.playerId = 1
    loginMsg = json.dumps(loginMsg.serialize())
    logoutMsg = PlayerLogoutInd()
    logoutMsg.playerId = 1
    logoutMsg = json.dumps(logoutMsg.serialize())
    msgReceiver.onMsgReceived(None, loginMsg)
    assert(len(players) == 1)
    msgReceiver.onMsgReceived(None, logoutMsg)
    assert(len(players) == 0)
    msgReceiver.deregister(InMsgs.PLAYER_LOGIN_IND)
    msgReceiver.onMsgReceived(None, loginMsg)
    assert(len(players) == 0)

