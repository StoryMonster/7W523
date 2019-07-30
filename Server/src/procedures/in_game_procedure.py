from fsm.fsm import FSM
from fsm.state import FsmFinalState, FsmState, DefaultInitState
from .client_events import TurnToNextPlayerDealEvent, DispatchCardsEvent, PassEvent, DealEvent
from messages.out_msgs import OutMsgs
import logging

def send_message(server, client, header, body):
    server.send_message(client, {"header": header, "body": body})

class GamingState(FsmState):
    def enter(self, event, fsm):
        if isinstance(event, DispatchCardsEvent):
            self.dispatch_cards(event, fsm)
        elif isinstance(event, TurnToNextPlayerDealEvent):
            self.change_the_deal_owner(event, fsm)
        elif isinstance(event, PassEvent):
            self.pass_this_turn(event, fsm)
        elif isinstance(event, DealEvent):
            self.deal(event, fsm)
        else:
            logging.error("Unknown event is triggered in game")
    
    def dispatch_cards(self, event, fsm):
        header = {"msgId": OutMsgs.CARDS_DISPATCH_IND, "playerId": fsm.context["playerId"], "roomId": fsm.context["roomId"]}
        body = {"cards": event.context["cards"]}
        send_message(fsm.context["server"], fsm.context["addr"], header, body)
    
    def change_the_deal_owner(self, event, fsm):
        header = {"msgId": OutMsgs.CHANGE_DEAL_OWNER_IND, "playerId": fsm.context["playerId"], "roomId": fsm.context["roomId"]}
        body = {"playerId": event.context["playerId"]}
        send_message(fsm.context["server"], fsm.context["addr"], header, body)

    def pass_this_turn(self, event, fsm):
        header = {"msgId": OutMsgs.PLAYER_PASS_IND, "playerId": fsm.context["playerId"], "roomId": fsm.context["roomId"]}
        body = {"playerId": event.context["playerId"]}
        send_message(fsm.context["server"], fsm.context["addr"], header, body)

    def deal(self, event, fsm):
        header = {"msgId": OutMsgs.PLAYER_DEAL_IND, "playerId": fsm.context["playerId"], "roomId": fsm.context["roomId"]}
        body = {"playerId": event.context["playerId"], "cards": event.context["cards"]}
        send_message(fsm.context["server"], fsm.context["addr"], header, body)


class InGameProcedure(FSM):
    def __init__(self, context):
        super().__init__(context)
        self.add_transaction(DefaultInitState, DispatchCardsEvent, GamingState)
        self.add_transaction(GamingState, TurnToNextPlayerDealEvent, GamingState)
        self.add_transaction(GamingState, DispatchCardsEvent, GamingState)
        self.add_transaction(GamingState, PassEvent, GamingState)
        self.add_transaction(GamingState, DealEvent, GamingState)
