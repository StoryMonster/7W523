import logging
from enum import IntEnum
from collections import namedtuple

class PlayerStatusInRoom(IntEnum):
    NotReady = 1
    Ready = 2
    Pass = 3
    WaitingEnemyDeal = 4
    Dealing = 5
    Calculating = 6        # 游戏结束，进行结算

PlayerInfoInRoom = namedtuple("PlayerInfoInRoom", ["player_id", "chair_no", "score", "status"])


class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.max_chairs_num = 2
        self.chairs = []

    def init_chairs(self):
        for i in range(self.max_chairs_num):
            self.chairs.append(None)  

    def are_chairs_full(self):
        return None not in self.chairs

    def get_room_id(self):
        return self.room_id

    def player_join(self, player_id):
        if self.are_chairs_full():
            logging.warn(f"{player_id} cannot join the room-{self.room_id}, this room is full")
            return
        for i in range(self.max_chairs_num):
            if self.chairs[i] is None:
                self.chairs[i] = PlayerInfoInRoom(player_id, i, 0, "NotReady")
        if player_id in self.players:
            logging.warn(f"{player_id} is already in thr room-{self.room_id}, cannot take in again")
            return
        self.players[player_id]
