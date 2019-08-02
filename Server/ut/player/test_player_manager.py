import pytest
from player.players_manager import PlayersManager
from msg.c2s_msgs import PlayerLoginInd, PlayerLogoutInd
from msg.msg_receiver import MsgReceiver


def test_handle_player_login(wsserver):
    playersMngr = PlayersManager(wsserver, MsgReceiver())
    playerLoginMsg = PlayerLoginInd()
    playerLoginMsg.playerId = 1
    playersMngr.handlePlayerLogin(playerLoginMsg, None)
    playerLoginMsg.playerId = 2
    playersMngr.handlePlayerLogin(playerLoginMsg, None)
    assert(len(playersMngr.players) == 2)

def test_handle_player_logout(wsserver):
    playersMngr = PlayersManager(wsserver, MsgReceiver())
    playerLoginMsg = PlayerLoginInd()
    playerLoginMsg.playerId = 1
    playersMngr.handlePlayerLogin(playerLoginMsg, None)
    playerLoginMsg.playerId = 2
    playersMngr.handlePlayerLogin(playerLoginMsg, None)
    playerLogoutMsg = PlayerLogoutInd()
    playerLogoutMsg.playerId = 1
    playersMngr.handlePlayerLogout(playerLogoutMsg, None)
    assert(len(playersMngr.players) == 1)

def test_handle_player_offline(wsserver):
    playersMngr = PlayersManager(wsserver, MsgReceiver())
    playerLoginMsg = PlayerLoginInd()
    playerLoginMsg.playerId = 1
    playersMngr.handlePlayerLogin(playerLoginMsg, None)
    playerLoginMsg.playerId = 2
    playersMngr.handlePlayerLogin(playerLoginMsg, None)
    playersMngr.handlePlayerOffline(1)
    assert(len(playersMngr.players) == 1)