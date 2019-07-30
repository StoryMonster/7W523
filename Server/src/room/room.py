import logging
from procedures.client_events import *

class PlayerInfoInRoom:
    def __init__(self, player):
        self.playerId = player.getId()
        self.score = 0
        self.cards = []
        self.isReady = False
        self.index = 0
        self.instance = player

    def getIndex(self):
        return self.index
    
    def process_event(self, event):
        self.instance.process_event(event)

    def getScore(self):
        reurn self.score
        

class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.max_players_num = 2
        self.players = {}

    def isRoomFull(self):
        return len(self.players) == self.max_players_num

    def get_room_id(self):
        return self.room_id

    def informNewComerRoomInfo(self, player):
        context = {"roomId": self.room_id, "otherPlayers": []}
        for playerId in self.players:
            context["otherPlayers"].append({"playerId": playerId, "index": self.players[playerId].getIndex()})
        player.process_event(EnterRoomEvent(context))
    
    def informOtherPlayersNewComerJoin(self, player, index):
        event = OnePlayerJoinEvent({"playerId": player.getId(), "index": index})
        for id in self.players:
            self.players[id].process_event(event)

    def informOtherPlayersSomeoneLeave(self, playerId):
        event = OnePlayerLeaveEvent({"playerId": player.getId()})
        for id in self.players:
            self.players[id].process_event(event)

    def informAllPlayersSomeoneReady(self, playerId):
        event = OnePlayerReadyEvent({"playerId": playerId})
        for id in self.players:
            self.players[id].process_event(event)

    def informAllPlayersSomeoneNotReady(self, playerId):
        event = OnePlayerNotReadyEvent({"playerId": playerId})
        for id in self.players:
            self.players[id].process_event(event)

    def informAllPlayersGameStart(self):
        event1 = AllPlayersReadyEvent({})
        event2 = GameStartEvent({})
        for id in self.players:
            self.players[id].process_event(event1)
            self.players[id].process_event(event2)

    def informAllPlayersGameOver(self):
        context = {"res": []}
        for id in self.players:
            context["res"].append({"playerId": id, "score": self.players[id].getScore()})
        event = GameOverEvent(context)
        for id in self.players:
            self.players[id].process_event(event)

    def informAllPlayersSomeoneDeal(self, playerId, cards):
        context = {"playerId": playerId, "cards": cards}
        event = DealEvent(context)
        for id in self.players:
            self.players[id].process_event(event)

    def informAllPlayersSomeonePass(self, playerId):
        event = PassEvent({"playerId": playerId})
        for id in self.players:
            self.players[id].process_event(event)

    def informAllPlayersDealOwnerChanger(self, playerId):
        event = TurnToNextPlayerDealEvent({"playerId": playerId})
        for id in self.players:
            self.players[id].process_event(event)

    def generateIndex(self):
        table = [0 for i in range(self.max_players_num)]
        for id in self.players:
            table[self.players[id].getIndex()] = 1
        for i in range(self.max_players_num):
            if table[i] == 0:
                return i
        return -1

    def player_join(self, player):
        if self.isRoomFull():
            logging.warn(f"this room is full")
            return
        self.informNewComerRoomInfo(player)
        player.process_event(PreGameEvent({}))
        index = self.generateIndex()
        self.informOtherPlayersNewComerJoin(player, index)
        self.players[player.getId()] = PlayerInfoInRoom(player)

    def player_leave(self, player):
        playerId = player.getId()
        if not self.isPlayerInRoom(playerId): return
        player.process_event(LeaveRoomEvent({}))
        del self.players[playerId]
        self.informOtherPlayersSomeoneLeave(playerId)

    def isPlayerInRoom(self, playerId):
        for playerInfo in self.playersInfos:
            if playerInfo.playerId == playerId:
                return True
        return False

    def isAllPlayersReady(self):
        for playerInfo in self.playersInfos:
            if playerInfo.isReady == False:
                return False
        return True

    def dispatchCardsToAllPlayers(self):
        pass

    def player_ready(self, player):
        if not self.isPlayerInRoom(player.getId()): return
        if self.isAllPlayersReady():
            self.informAllPlayersGameStart()
            self.dispatchCardsToAllPlayers()
        else:
            self.informAllPlayersSomeoneReady(player.getId())
    
    def player_not_ready(self, player):
        if not self.isPlayerInRoom(player.getId()): return
        self.informAllPlayersSomeoneNotReady(player.getId())
        

            
