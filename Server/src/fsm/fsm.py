from fsm_exceptions import FsmException
from state import FsmState, FsmFinalState
from event import FsmEvent
from collections import namedtuple
import logging

Transaction = namedtuple("Transaction", ["prev_state", "event", "next_state"])

class FSM:
    def __init__(self):
        self.state_transaction_table = []
        self.global_transaction_table = []
        self.current_state = None
        self.working_state = FsmState

    def add_global_transaction(self, event, end_state):     # 全局转换，直接进入到结束状态
        if not issubclass(end_state, FsmFinalState):
            raise FsmException("The state should be FsmFinalState")
        self.global_transaction_table.append(Transaction(self.working_state, event, end_state))

    def add_transaction(self, prev_state, event, next_state):
        if issubclass(prev_state, FsmFinalState):
            raise FsmException("It's not allowed to add transaction after Final State Node")
        self.state_transaction_table.append(Transaction(prev_state, event, next_state))

    def process_event(self, event):
        for transaction in self.global_transaction_table:
            if isinstance(event, transaction.event):
                self.current_state = transaction.next_state()
                self.current_state.enter(event)
                self.clear_transaction_table()
                return
        for transaction in self.state_transaction_table:
            if isinstance(self.current_state, transaction.prev_state) and isinstance(event, transaction.event):
                self.current_state.leave()
                self.current_state = transaction.next_state()
                self.current_state.enter(event)
                if isinstance(self.current_state, FsmFinalState):
                    self.clear_transaction_table()
                return
        raise FsmException("Transaction not found")
    
    def clear_transaction_table(self):
        self.global_transaction_table = []
        self.state_transaction_table = []

    def run(self):
        if len(self.state_transaction_table) == 0: return
        self.current_state = self.state_transaction_table[0].prev_state()
        self.current_state.enter(None)

class EvtOpen(FsmEvent):
    def __init__(self, context):
        super().__init__(context)

class EvtPause(FsmEvent):
    def __init__(self, context):
        super().__init__(context)

class EvtClose(FsmEvent):
    def __init__(self, context):
        super().__init__(context)

class StateSleeping(FsmState):
    def enter(self, event):
        print("enter StateSleeping")

    def leave(self):
        print("leave StateSleeping")

class StateRunning(FsmState):
    def enter(self, event):
        print("enter StateRunning")

    def leave(self):
        print("leave StateRunning")

class StatePause(FsmState):
    def enter(self, event):
        print("enter StatePause")

    def leave(self):
        print("leave StatePause")

class StateShutdown(FsmFinalState):
    def enter(self, event):
        print("enter StateShutdown")

if __name__ == "__main__":
    fsm = FSM()
    #fsm.add_global_transaction(EvtClose, StateShutdown)
    fsm.add_transaction(StateSleeping, EvtOpen, StateRunning)
    fsm.add_transaction(StateRunning, EvtClose, StateShutdown)
    fsm.add_transaction(StateRunning, EvtPause, StatePause)
    fsm.add_transaction(StatePause, EvtOpen, StateRunning)
    fsm.add_transaction(StatePause, EvtClose, StateShutdown)

    fsm.run()
    fsm.process_event(EvtOpen(None))
    fsm.process_event(EvtPause(None))
   # fsm.process_event(EvtClose(None))
    fsm.process_event(EvtOpen(None))
    fsm.process_event(EvtPause(None))
    fsm.process_event(EvtClose(None))
    #fsm.process_event(EvtPause(None))
