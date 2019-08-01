from enum import IntEnum

class OutMsgs(IntEnum):
    DISPATCH_CARDS_IND = 1
    GAME_OVER_IND = 2
    GAME_START_IND = 3
    PLAYER_DEAL_IND = 4
    PLAYER_PASS_IND = 5
    PLAYER_GET_SCORE_IND = 6
    ROOM_INFO_IND = 7
    PLAYER_JOIN_ROOM_IND = 8
    PLAYER_LEAVE_ROOM_IND = 9
    PLAYER_READY_IND = 10
    DEAL_OWNER_CHANGE_IND = 11