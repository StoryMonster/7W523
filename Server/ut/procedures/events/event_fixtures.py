from procedures.client_events import *
import pytest

@pytest.fixture
def onePlayerReadyEvent():
    context = {"playerId": 11, "roomId": 10}
    return OnePlayerReadyEvent(context)

@pytest.fixture
def onePlayerNotReadyEvent():
    context = {"playerId": 11, "roomId": 10}
    return OnePlayerNotReadyEvent(context)

@pytest.fixture
def allPlayersReadyEvent():
    context = {"roomId": 10}
    return AllPlayersReadyEvent(context)

@pytest.fixture
def onePlayerJoinEvent():
    context = {"playerId": 11, "roomId": 10}
    return OnePlayerJoinEvent(context)

@pytest.fixture
def onePlayerLeaveEvent():
    context = {"playerId": 11, "roomId": 10}
    return OnePlayerLeaveEvent(context)

@pytest.fixture
def replayEvent():
    return ReplayEvent({})

@pytest.fixture
def turnToNextPlayerDealEvent():
    return TurnToNextPlayerDealEvent({})

@pytest.fixture
def dispatchCardsEvent():
    return DispatchCardsEvent({})

@pytest.fixture
def offlineEvent():
    return OfflineEvent({})

@pytest.fixture
def logoutEvent():
    return LogoutEvent({})

@pytest.fixture
def preGameEvent():
    return PreGameEvent({})

@pytest.fixture
def gameStartEvent():
    return GameStartEvent({})

@pytest.fixture
def leaveRoomEvent():
    return LeaveRoomEvent({})

@pytest.fixture
def gameOverEvent():
    return GameOverEvent({})

@pytest.fixture
def dealEvent():
    return DealEvent({})

@pytest.fixture
def passEvent():
    return PassEvent({})

@pytest.fixture
def dealTimeoutEvent():
    return DealTimeoutEvent({})

@pytest.fixture
def enterRoomEvent():
    return EnterRoomEvent({"roomId": -1, "playerId": 1})