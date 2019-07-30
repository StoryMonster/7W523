from fsm.fsm import FSM
from fsm.state import DefaultInitState, FsmState, FsmFinalState
from .client_events import AllPlayersReadyEvent, OnePlayerReadyEvent, OnePlayerNotReadyEvent, OnePlayerJoinEvent, OnePlayerLeaveEvent
from messages.out_msgs import OutMsgs
import logging

def send_player_join_room_ind(server, client, player_id, other_player_id, roomId):
    header = {"msgId": OutMsgs.PLAYER_JOIN_ROOM_IND, "playerId": player_id, "roomId": roomId}
    body = {"playerId": other_player_id}
    server.send_msg(client, {"header": header, "body": body})

def send_player_leave_room_ind(server, client, player_id, other_player_id, roomId):
    header = {"msgId": OutMsgs.PLAYER_LEAVE_ROOM_IND, "playerId": player_id, "roomId": roomId}
    body = {"playerId": other_player_id}
    server.send_msg(client, {"header": header, "body": body})

def send_player_ready_ind(server, client, player_id, other_player_id, roomId):
    header = {"msgId": OutMsgs.PLAYER_READY_IND, "playerId": player_id, "roomId": roomId}
    body = {"playerId": other_player_id}
    server.send_msg(client, {"header": header, "body": body})

def send_player_not_ready_ind(server, client, player_id, other_player_id, roomId):
    header = {"msgId": OutMsgs.PLAYER_NOT_READY_IND, "playerId": player_id, "roomId": roomId}
    body = {"playerId": other_player_id}
    server.send_msg(client, {"header": header, "body": body})

def send_game_start_ind(server, client, player_id, roomId):
    header = {"msgId": OutMsgs.GameStartInd, "playerId": player_id, "roomId": roomId}
    body = {}
    server.send_msg(client, {"header": header, "body": body})

class WaitForPlayersReadyState(FsmState):
    def enter(self, event, fsm):
        if isinstance(event, OnePlayerReadyEvent):
            send_player_ready_ind(fsm.context["server"], fsm.context["addr"], fsm.context["playerId"],
                                  event.context["playerId"], fsm.context["roomId"])
            logging.debug(f"{event.context['playerId']} is ready")
        elif isinstance(event, OnePlayerNotReadyEvent):
            send_player_not_ready_ind(fsm.context["server"], fsm.context["addr"], fsm.context["playerId"],
                                  event.context["playerId"], fsm.context["roomId"])
            logging.debug(f"{event.context['playerId']} is not ready")
        elif isinstance(event, OnePlayerJoinEvent):
            send_player_join_room_ind(fsm.context["server"], fsm.context["addr"], fsm.context["playerId"],
                                      event.context["playerId"], fsm.context["roomId"])
            logging.debug(f"{event.context['playerId']} enter the room")
        elif isinstance(event, OnePlayerLeaveEvent):
            send_player_leave_room_ind(fsm.context["server"], fsm.context["addr"], fsm.context["playerId"],
                                       event.context["playerId"], fsm.context["roomId"])
            logging.debug(f"{event.context['playerId']} leave the room")
        else:
            logging.error("Unknown event received when waiting for all players ready")

class GameStartState(FsmFinalState):
    def enter(self, event, fsm):
        logging.debug("The game is ready to start")
        send_game_start_ind(fsm.context["server"], fsm.context["addr"], fsm.context["playerId"], fsm.context["roomId"])

class PreGameProcedure(FSM):
    def __init__(self, context):
        super().__init__(context)
        self.add_global_transaction(AllPlayersReadyEvent, GameStartState)
        self.add_transaction(DefaultInitState, OnePlayerReadyEvent, WaitForPlayersReadyState)
        self.add_transaction(DefaultInitState, OnePlayerNotReadyEvent, WaitForPlayersReadyState)
        self.add_transaction(DefaultInitState, OnePlayerJoinEvent, WaitForPlayersReadyState)
        self.add_transaction(DefaultInitState, OnePlayerLeaveEvent, WaitForPlayersReadyState)
        self.add_transaction(WaitForPlayersReadyState, OnePlayerReadyEvent, WaitForPlayersReadyState)
        self.add_transaction(WaitForPlayersReadyState, OnePlayerNotReadyEvent, WaitForPlayersReadyState)
        self.add_transaction(WaitForPlayersReadyState, OnePlayerJoinEvent, WaitForPlayersReadyState)
        self.add_transaction(WaitForPlayersReadyState, OnePlayerLeaveEvent, WaitForPlayersReadyState)
        