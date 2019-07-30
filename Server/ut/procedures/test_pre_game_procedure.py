import pytest
from procedures.pre_game_procedure import *
from events.event_fixtures import *

@pytest.fixture
def pregameProcedure():
    context = {"playerId": 1, "roomId": 2}
    procedure = PreGameProcedure(context)
    procedure.run()
    return procedure

def test_received_one_player_ready_event(pregameProcedure, onePlayerReadyEvent):
    pregameProcedure.process_event(onePlayerReadyEvent)
    assert(isinstance(pregameProcedure.current_state, WaitForPlayersReadyState))
    onePlayerReadyEvent.context["playerId"] = 13
    pregameProcedure.process_event(onePlayerReadyEvent)
    assert(isinstance(pregameProcedure.current_state, WaitForPlayersReadyState))

def test_received_one_player_not_ready_event(pregameProcedure, onePlayerReadyEvent, onePlayerNotReadyEvent):
    pregameProcedure.process_event(onePlayerReadyEvent)
    assert(isinstance(pregameProcedure.current_state, WaitForPlayersReadyState))
    pregameProcedure.process_event(onePlayerNotReadyEvent)
    assert(isinstance(pregameProcedure.current_state, WaitForPlayersReadyState))

def test_received_one_player_join_event(pregameProcedure, onePlayerJoinEvent):
    pregameProcedure.process_event(onePlayerJoinEvent)
    assert(isinstance(pregameProcedure.current_state, WaitForPlayersReadyState))
    pregameProcedure.process_event(onePlayerJoinEvent)
    assert(isinstance(pregameProcedure.current_state, WaitForPlayersReadyState))

def test_received_one_player_leave_event(pregameProcedure, onePlayerLeaveEvent):
    pregameProcedure.process_event(onePlayerLeaveEvent)
    assert(isinstance(pregameProcedure.current_state, WaitForPlayersReadyState))
    pregameProcedure.process_event(onePlayerLeaveEvent)
    assert(isinstance(pregameProcedure.current_state, WaitForPlayersReadyState))

def test_received_all_players_ready_event(pregameProcedure, onePlayerJoinEvent, allPlayersReadyEvent):
    pregameProcedure.process_event(onePlayerJoinEvent)
    assert(isinstance(pregameProcedure.current_state, WaitForPlayersReadyState))
    pregameProcedure.process_event(allPlayersReadyEvent)
    assert(pregameProcedure.current_state is None)