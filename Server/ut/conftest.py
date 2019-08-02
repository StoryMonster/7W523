import pytest
from lib.ws_server import WsServer
from lib.ws_client import WsClient
from lib.fake_player import FakePlayer

MAX_PLAYERS_NUM = 3

@pytest.fixture
def wsserver():
    return WsServer()


@pytest.fixture
def players(wsserver):
    players = []
    for i in range(MAX_PLAYERS_NUM):
        players.append(FakePlayer(i+1, WsClient(), wsserver))
        players[i].login()
    return players

