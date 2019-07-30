from fsm.fsm import FSM
from fsm.state import FsmState, FsmFinalState, DefaultInitState
from .client_events import EnterRoomEvent
from messages.out_msgs import OutMsgs
import logging

def send_room_info_ind(server, client, player_id, room_id, otherPlayers):
    header = {"msgId": OutMsgs.ROOM_INFO_IND, "playerId": player_id}
    body = {"roomId": room_id, "otherPlayers": otherPlayers}
    server.send_message(client, {"header": header, "body": body})

class EnterRoomState(FsmFinalState):
    def enter(self, event, fsm):
        fsm.context["roomId"] = event.context["roomId"]
        logging.debug(f"{fsm.context['playerId']} joint room-{fsm.context['roomId']}")
        send_room_info_ind(fsm.context["server"], fsm.context["addr"], fsm.context["playerId"], fsm.context["roomId"], event.context[otherPlayers])

class WaitRoomChooseProcedure(FSM):
    def __init__(self, context):
        super().__init__(context)
        self.add_transaction(DefaultInitState, EnterRoomEvent, EnterRoomState)
