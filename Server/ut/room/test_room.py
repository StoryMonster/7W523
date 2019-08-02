import pytest
import json
from room.room import Room
from common.room_types import RoomType
from player.player import Player
from msg.s2c_msgs import RoomInfoInd, PlayerJoinRoomInd, PlayerLeaveRoomInd, PlayerReadyInd, GameStartInd, DealOwnerChangeInd


def test_player_join_room(wsserver, players):
    room = Room(1, wsserver, RoomType.ThreePlayersRoom)
    ## first player join
    room.handlePlayerJoinRoom(players[0])
    expectRoomInfoInd = {"msgId": RoomInfoInd().msgId, "players": [{"playerId": 1, "roomId": 1, "index": 0, "isReady": False}]}
    assert(players[0].receive() == expectRoomInfoInd)
    assert(not room.isFull())
    ## second player join
    room.handlePlayerJoinRoom(players[1])
    expectRoomInfoInd = {"msgId": RoomInfoInd().msgId, "players": [{"playerId": 1, "roomId": 1, "index": 0, "isReady": False},
                                                                   {"playerId": 2, "roomId": 1, "index": 1, "isReady": False}]}
    expectPlayerJoinRoomInd = {"msgId": PlayerJoinRoomInd().msgId, "playerInfo": {"playerId": 2, "roomId": 1, "index": 1, "isReady": False}}
    assert(players[1].receive() == expectRoomInfoInd)
    assert(players[0].receive() == expectPlayerJoinRoomInd)
    assert(not room.isFull())
    ## third player join
    room.handlePlayerJoinRoom(players[2])
    expectRoomInfoInd = {"msgId": RoomInfoInd().msgId, "players": [{"playerId": 1, "roomId": 1, "index": 0, "isReady": False},
                                                                   {"playerId": 2, "roomId": 1, "index": 1, "isReady": False},
                                                                   {"playerId": 3, "roomId": 1, "index": 2, "isReady": False}]}
    expectPlayerJoinRoomInd = {"msgId": PlayerJoinRoomInd().msgId, "playerInfo": {"playerId": 3, "roomId": 1, "index": 2, "isReady": False}}
    assert(players[2].receive() == expectRoomInfoInd)
    assert(players[0].receive() == expectPlayerJoinRoomInd)
    assert(players[1].receive() == expectPlayerJoinRoomInd)
    assert(room.isFull())


def test_player_leave_room(wsserver, players):
    room = Room(1, wsserver, RoomType.ThreePlayersRoom)
    room.handlePlayerJoinRoom(players[0])
    room.handlePlayerJoinRoom(players[1])
    room.handlePlayerJoinRoom(players[2])
    assert(room.isFull())
    ## first player leave room
    room.handlePlayerLeaveRoom(players[0])
    expectPlayerLeaveRoomInd = {"msgId": PlayerLeaveRoomInd().msgId, "playerInfo": {"playerId": 1, "roomId": 1, "index": 0, "isReady": False}}
    assert(players[1].latest_receive() == expectPlayerLeaveRoomInd)
    assert(players[2].latest_receive() == expectPlayerLeaveRoomInd)
    ## second player leave room
    room.handlePlayerLeaveRoom(players[1])
    expectPlayerLeaveRoomInd = {"msgId": PlayerLeaveRoomInd().msgId, "playerInfo": {"playerId": 2, "roomId": 1, "index": 1, "isReady": False}}
    assert(players[2].latest_receive() == expectPlayerLeaveRoomInd)
    ## third player leave room
    room.handlePlayerLeaveRoom(players[2])
    expectPlayerLeaveRoomInd = {"msgId": PlayerLeaveRoomInd().msgId, "playerInfo": {"playerId": 3, "roomId": 1, "index": 2, "isReady": False}}
    assert(room.isEmpty())

def test_player_ready(wsserver, players):
    room = Room(1, wsserver, RoomType.TwoPlayersRoom)
    room.handlePlayerJoinRoom(players[0])
    room.handlePlayerJoinRoom(players[1])
    room.handlePlayerReady(players[0])
    expectPlayerReadyInd = {"msgId": PlayerReadyInd().msgId, "playerInfo": {"playerId": 1, "roomId": 1, "index": 0, "isReady": True}}
    assert(players[0].latest_receive() == expectPlayerReadyInd)
    assert(players[1].latest_receive() == expectPlayerReadyInd)
    room.handlePlayerReady(players[0])
    expectPlayerReadyInd = {"msgId": PlayerReadyInd().msgId, "playerInfo": {"playerId": 1, "roomId": 1, "index": 0, "isReady": False}}
    assert(players[0].latest_receive() == expectPlayerReadyInd)
    assert(players[1].latest_receive() == expectPlayerReadyInd)
    room.handlePlayerReady(players[0])
    assert(players[0].latest_receive() == {"msgId": PlayerReadyInd().msgId, "playerInfo": {"playerId": 1, "roomId": 1, "index": 0, "isReady": True}})
    assert(players[1].latest_receive() == {"msgId": PlayerReadyInd().msgId, "playerInfo": {"playerId": 1, "roomId": 1, "index": 0, "isReady": True}})
    room.handlePlayerReady(players[1])
    assert(players[0].receive() == {"msgId": PlayerReadyInd().msgId, "playerInfo": {"playerId": 2, "roomId": 1, "index": 1, "isReady": True}})
    assert(players[1].receive() == {"msgId": PlayerReadyInd().msgId, "playerInfo": {"playerId": 2, "roomId": 1, "index": 1, "isReady": True}})
    expectGameStartInd = {"msgId": GameStartInd().msgId, "roomId": 1}
    assert(players[0].receive() == expectGameStartInd)
    assert(players[1].receive() == expectGameStartInd)
    players[0].receive()
    players[1].receive()
    assert(players[0].latest_receive() == {"msgId": DealOwnerChangeInd().msgId, "playerId": 1, "roomId": 1})
    assert(players[1].latest_receive() == {"msgId": DealOwnerChangeInd().msgId, "playerId": 1, "roomId": 1})

def test_dispatch_cards(wsserver, players):
    room = Room(1, wsserver, RoomType.TwoPlayersRoom)
    room.handlePlayerJoinRoom(players[0])
    room.handlePlayerJoinRoom(players[1])
    room.players[1].cards = [1, 2, 3]
    room.dispatchCards()
    assert(len(players[0].latest_receive()["cards"]) == 2)
    assert(len(players[1].latest_receive()["cards"]) == 5)

def test_player_deal(wsserver, players):
    room = Room(1, wsserver, RoomType.TwoPlayersRoom)
    room.handlePlayerJoinRoom(players[0])
    room.handlePlayerJoinRoom(players[1])
    room.handlePlayerReady(players[0])
    room.handlePlayerReady(players[1])
    players[0].latest_receive()
    players[1].latest_receive()
    room.handlePlayerDeal(players[0], room.players[1].cards[:2])
    assert(len(players[0].receive()["cards"]) == 2)
    assert(len(players[1].receive()["cards"]) == 2)
    assert(players[0].latest_receive() == {"msgId": DealOwnerChangeInd().msgId, "playerId": 2, "roomId": 1})
    assert(players[1].latest_receive() == {"msgId": DealOwnerChangeInd().msgId, "playerId": 2, "roomId": 1})
    assert(len(room.players[1].cards) == 3)

def test_player_deal_triggrt_new_round(wsserver, players):
    room = Room(1, wsserver, RoomType.TwoPlayersRoom)
    room.handlePlayerJoinRoom(players[0])
    room.handlePlayerJoinRoom(players[1])
    room.handlePlayerReady(players[0])
    room.handlePlayerReady(players[1])
    players[0].latest_receive()
    players[1].latest_receive()
    room.players[1].cards = [1]
    room.players[2].cards = []
    room.players[2].isPassing = True
    room.handlePlayerDeal(players[0], [1])
    assert(len(players[0].receive()["cards"]) == 1)
    assert(len(players[1].receive()["cards"]) == 1)
    assert(len(players[0].receive()["cards"]) == 5)
    assert(len(players[1].receive()["cards"]) == 5)
    assert(len(room.players[1].cards) == 5)
    assert(len(room.players[2].cards) == 5)
    assert(room.currentDealIndex == 0)

def test_player_pass(wsserver, players):
    room = Room(1, wsserver, RoomType.TwoPlayersRoom)
    room.handlePlayerJoinRoom(players[0])
    room.handlePlayerJoinRoom(players[1])
    room.handlePlayerReady(players[0])
    room.handlePlayerReady(players[1])
    assert(len(room.players[1].cards) == 5)
    assert(len(room.players[2].cards) == 5)
    room.handlePlayerDeal(players[0], room.players[1].cards[:2])
    players[0].latest_receive()
    players[1].latest_receive()
    room.handlePlayerPass(players[1])
    assert(len(room.players[1].cards) == 5)
    assert(len(room.players[2].cards) == 5)
    assert(room.currentDealIndex == 0)

def test_player_deal_timeout(wsserver, players):
    room = Room(1, wsserver, RoomType.TwoPlayersRoom)
    room.handlePlayerJoinRoom(players[0])
    room.handlePlayerJoinRoom(players[1])
    room.handlePlayerReady(players[0])
    room.handlePlayerReady(players[1])
    assert(len(room.players[1].cards) == 5)
    assert(len(room.players[2].cards) == 5)
    room.handlePlayerDeal(players[0], room.players[1].cards[:2])
    players[0].latest_receive()
    players[1].latest_receive()
    room.handlePlayerDealTimeout(players[1])
    assert(len(room.players[1].cards) == 5)
    assert(len(room.players[2].cards) == 5)
    assert(room.currentDealIndex == 0)


