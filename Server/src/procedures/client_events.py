from fsm.event import FsmEvent

class EnterRoomEvent(FsmEvent):
    pass

class LeaveRoomEvent(FsmEvent):
    pass

class AllPlayersReadyEvent(FsmEvent):
    pass

class OnePlayerReadyEvent(FsmEvent):
    pass

class OnePlayerNotReadyEvent(FsmEvent):
    pass

class OnePlayerJoinEvent(FsmEvent):
    pass

class OnePlayerLeaveEvent(FsmEvent):
    pass

class ReplayEvent(FsmEvent):
    pass

class PreGameEvent(FsmEvent):
    pass

class GameOverEvent(FsmEvent):
    pass

class GameStartEvent(FsmEvent):
    pass

class TurnToNextPlayerDealEvent(FsmEvent):
    pass

class DispatchCardsEvent(FsmEvent):
    pass

class LogoutEvent(FsmEvent):
    pass

class OfflineEvent(FsmEvent):
    pass

class PassEvent(FsmEvent):
    pass

class DealEvent(FsmEvent):
    pass