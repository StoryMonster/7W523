from procedures.wait_room_choose_procedure import *
from events.event_fixtures import *

@pytest.fixture
def waitRoomChooseProcedure():
    context = {"roomId": 0, "playerId": 12}
    procedure = WaitRoomChooseProcedure(context)
    procedure.run()
    return procedure

def test_received_enter_room_event(waitRoomChooseProcedure, enterRoomEvent):
    waitRoomChooseProcedure.process_event(enterRoomEvent)
    assert(waitRoomChooseProcedure.context["roomId"] == enterRoomEvent.context["roomId"])

