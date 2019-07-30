
from fsm.fsm import FSM
from fsm.event import FsmEvent
from fsm.state import FsmState, FsmFinalState
from procedures.wait_room_choose_procedure import *
from procedures.pre_game_procedure import *
from procedures.in_game_procedure import *
from procedures.post_game_procedure import *
from .client_events import OfflineEvent, LogoutEvent, PreGameEvent, GameStartEvent, LeaveRoomEvent, GameOverEvent
import logging

class OfflineState(FsmFinalState):
    def enter(self, event, fsm):
        playerId = fsm.context["playerId"]
        logging.debug(f"{playerId} offline")
        fsm.current_procedure = None

class LogoutState(FsmFinalState):
    def enter(self, event, fsm):
        playerId = fsm.context["playerId"]
        logging.debug(f"{playerId} logout")
        fsm.current_procedure = None

class PlayerChooseRoomState(FsmState):
    def enter(self, event, fsm):
        playerId = fsm.context["playerId"]
        logging.debug(f"{playerId} is choosing the room")
        fsm.current_procedure = None
        fsm.current_procedure = WaitRoomChooseProcedure(fsm.context)
        fsm.current_procedure.run()

class PreGameState(FsmState):
    def enter(self, event, fsm):
        playerId = fsm.context["playerId"]
        logging.debug(f"{playerId} is waiting game start")
        fsm.current_procedure = None
        fsm.current_procedure = PreGameProcedure(fsm.context)
        fsm.current_procedure.run()

class InGameState(FsmState):
    def enter(self, event, fsm):
        playerId = fsm.context["playerId"]
        logging.debug(f"{playerId} start game")
        fsm.current_procedure = None
        fsm.current_procedure = InGameProcedure(fsm.context)
        fsm.current_procedure.run()

class PostGameState(FsmState):
    def enter(self, event, fsm):
        playerId = fsm.context["playerId"]
        logging.debug(f"{playerId} game over")
        fsm.current_procedure = None
        fsm.current_procedure = PostGameProcedure(fsm.context)
        fsm.current_procedure.run()

class ClientGlobalProcedure(FSM):
    def __init__(self, context):
        super().__init__(context)
        self.current_procedure = None
        self.add_global_transaction(OfflineEvent, OfflineState)
        self.add_global_transaction(LogoutEvent, LogoutState)
        self.add_transaction(PlayerChooseRoomState, PreGameEvent, PreGameState)
        self.add_transaction(PreGameState, GameStartEvent, InGameState)
        self.add_transaction(PreGameState, LeaveRoomEvent, PlayerChooseRoomState)
        self.add_transaction(InGameState, GameOverEvent, PostGameState)
        self.add_transaction(InGameState, LeaveRoomEvent, PlayerChooseRoomState)
        self.add_transaction(PostGameState, LeaveRoomEvent, PlayerChooseRoomState)
    
    def process_event(self, event):
        next_state = self.next_state(event)
        if (next_state is None) and (self.current_procedure is not None) and (self.current_procedure.isRunning()):
            self.current_procedure.process_event(event)
        else:
            super().process_event(event)
