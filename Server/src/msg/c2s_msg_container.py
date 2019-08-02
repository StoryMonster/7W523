from .in_msgs import InMsgs
from .c2s_msgs import *

class C2SMsgContainer:
    def __init__(self):
        self.templates = {
            InMsgs.PLAYER_LOGIN_IND: PlayerLoginInd,
            InMsgs.PLAYER_LOGOUT_IND: PlayerLogoutInd,
            InMsgs.PLAYER_ENTER_ROOM_IND: PlayerEnterRoomInd,
            InMsgs.PLAYER_LEAVE_ROOM_IND: PlayerLeaveRoomInd,
            InMsgs.PLAYER_READY_IND: PlayerReadyInd,
            InMsgs.PLAYER_PASS_IND: PlayerPassInd,
            InMsgs.PLAYER_DEAL_IND: PlayerDealInd,
            InMsgs.PLAYER_DEAL_TIMEOUT_IND: PlayerDealTimeoutInd
        }

    def getTemplate(self, msgId):
        if msgId in self.templates:
            return self.templates[msgId]
        return None