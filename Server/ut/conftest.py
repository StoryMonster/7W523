import pytest
from lib.ws_server import WsServer
from lib.ws_client import WsClient


@pytest.fixture
def wsserver():
    return WsServer()

@pytest.fixture
def wsclient():
    return WsClient()