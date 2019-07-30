from fsm.fsm import FSM
from fsm.state import FsmFinalState, FsmState, DefaultInitState
from .client_events import ReplayEvent
import logging

class ReplayState(FsmFinalState):
    def enter(self, event, fsm):
        logging.debug(f"{fsm.context['playerId']} is going to stay at the room")

class PostGameProcedure(FSM):
    def __init__(self, context):
        super().__init__(context)
        self.add_transaction(DefaultInitState, ReplayEvent, ReplayState)