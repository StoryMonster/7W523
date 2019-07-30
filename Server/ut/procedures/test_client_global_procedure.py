import pytest
from procedures.client_global_procedure import ClientGlobalProcedure
from events.event_fixtures import *

@pytest.fixture
def clientGlobalProcedure():
    context = {"playerId": 1, "roomId": -1}
    procedure = ClientGlobalProcedure(context)
    procedure.run()
    return procedure

def test_received_logout_event(clientGlobalProcedure, logoutEvent, preGameEvent):
    clientGlobalProcedure.process_event(preGameEvent)
    clientGlobalProcedure.process_event(logoutEvent)
    assert(not clientGlobalProcedure.isRunning())

def test_received_offline_event(clientGlobalProcedure, offlineEvent, preGameEvent):
    clientGlobalProcedure.process_event(preGameEvent)
    clientGlobalProcedure.process_event(offlineEvent)
    assert(not clientGlobalProcedure.isRunning())

def test_normal_client_running_procedure(clientGlobalProcedure, enterRoomEvent, preGameEvent, onePlayerReadyEvent, allPlayersReadyEvent,
                                         gameStartEvent, dispatchCardsEvent, turnToNextPlayerDealEvent, dealEvent, passEvent, gameOverEvent,
                                         leaveRoomEvent, logoutEvent):
    enterRoomEvent.context["roomId"] = 13
    clientGlobalProcedure.process_event(enterRoomEvent)
    assert(clientGlobalProcedure.context["roomId"] == enterRoomEvent.context["roomId"])
    clientGlobalProcedure.process_event(preGameEvent)
    clientGlobalProcedure.process_event(onePlayerReadyEvent)
    clientGlobalProcedure.process_event(allPlayersReadyEvent)
    clientGlobalProcedure.process_event(gameStartEvent)
    clientGlobalProcedure.process_event(dispatchCardsEvent)
    clientGlobalProcedure.process_event(turnToNextPlayerDealEvent)
    clientGlobalProcedure.process_event(dealEvent)
    clientGlobalProcedure.process_event(turnToNextPlayerDealEvent)
    clientGlobalProcedure.process_event(passEvent)
    clientGlobalProcedure.process_event(gameOverEvent)
    clientGlobalProcedure.process_event(leaveRoomEvent)
    clientGlobalProcedure.process_event(logoutEvent)
    assert(not clientGlobalProcedure.isRunning())
