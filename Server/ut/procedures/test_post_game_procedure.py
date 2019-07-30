import pytest
from procedures.post_game_procedure import *
from events.event_fixtures import *

@pytest.fixture
def postGameProcedure():
    context = {"playerId": 1, "roomId": 2}
    procedure = PostGameProcedure(context)
    procedure.run()
    return procedure

def test_received_replay_event(postGameProcedure, replayEvent):
    postGameProcedure.process_event(replayEvent)
    assert(not postGameProcedure.isRunning())