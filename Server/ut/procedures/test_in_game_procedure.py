import pytest
from procedures.in_game_procedure import *
from events.event_fixtures import *


@pytest.fixture
def inGameProcedure():
    context = {"playerId": 1, "roomId":2}
    procedure = InGameProcedure(context)
    procedure.run()
    return procedure

def test_received_dispatch_cards_event(inGameProcedure, dispatchCardsEvent):
    inGameProcedure.process_event(dispatchCardsEvent)
    assert(isinstance(inGameProcedure.current_state, GamingState))

def test_received_turn_to_next_player_deal_event(inGameProcedure, dispatchCardsEvent, turnToNextPlayerDealEvent):
    inGameProcedure.process_event(dispatchCardsEvent)
    inGameProcedure.process_event(turnToNextPlayerDealEvent)
    assert(isinstance(inGameProcedure.current_state, GamingState))

def test_received_pass_event(inGameProcedure, dispatchCardsEvent, turnToNextPlayerDealEvent, passEvent):
    inGameProcedure.process_event(dispatchCardsEvent)
    inGameProcedure.process_event(turnToNextPlayerDealEvent)
    inGameProcedure.process_event(passEvent)
    assert(isinstance(inGameProcedure.current_state, GamingState))

def test_received_deal_event(inGameProcedure, dispatchCardsEvent, turnToNextPlayerDealEvent, dealEvent):
    inGameProcedure.process_event(dispatchCardsEvent)
    inGameProcedure.process_event(turnToNextPlayerDealEvent)
    inGameProcedure.process_event(dealEvent)
    assert(isinstance(inGameProcedure.current_state, GamingState))
