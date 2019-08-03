from .player_in_room import PlayerInRoom
from cards.card_heap import CardHeap
from msg.s2c_msgs import *
from common.room_types import RoomType
import logging

class Room:
### public
    def __init__(self, roomId, ws_server, roomType):
        self.roomId = roomId
        self.ws_server = ws_server
        self.roomType = roomType
        self.maxPlayerNum = 2
        if roomType == RoomType.ThreePlayersRoom:
            self.maxPlayerNum = 3
        self.cardHeap = CardHeap()
        self.players = {}
        self.currentDealIndex = 0
        self.lastDealIndex = 0
        self.scoreInRound = 0
    
    def handlePlayerJoinRoom(self, player):
        playerId = player.playerId
        if self.isPlayerInRoom(playerId):
            logging.error(f"player {playerId} is already in room {self.roomId}")
        else:
            index = self.generatePlayerIndex()
            self.players[playerId] = PlayerInRoom(player, index)
        logging.info(f"player {playerId} enter room {self.roomId}")
        self.sendRoomInfoInd(player)
        msg = PlayerJoinRoomInd()
        msg.playerInfo = PublicPlayerInfoInRoom(playerId, self.roomId, self.players[playerId].index, self.players[playerId].isReady)
        self.sendToAllExcept(playerId, msg)

    def handlePlayerLeaveRoom(self, player):
        playerId = player.playerId
        if not self.isPlayerInRoom(playerId):
            logging.error(f"player {playerId} is not in room {self.roomId}")
            return
        msg = PlayerLeaveRoomInd()
        msg.playerInfo = PublicPlayerInfoInRoom(playerId, self.roomId, self.players[playerId].index, self.players[playerId].isReady)
        del self.players[playerId]
        logging.info(f"player {playerId} left room {self.roomId}")
        self.broadcast(msg)

    def handlePlayerReady(self, player):
        playerId = player.playerId
        if not self.isPlayerInRoom(playerId):
            logging.error(f"player {playerId} is not in room {self.roomId}")
            return
        self.players[playerId].isReady = not self.players[playerId].isReady
        logging.info(f"player {playerId} changed ready status in room {self.roomId}, ready: {self.players[playerId].isReady}")
        msg = PlayerReadyInd()
        msg.playerInfo = PublicPlayerInfoInRoom(playerId, self.roomId, self.players[playerId].index, self.players[playerId].isReady)
        self.broadcast(msg)
        if self.areAllPlayersReady():
            self.startGame()

    def handlePlayerDeal(self, player, cards):
        playerId = player.playerId
        if not self.isPlayerInRoom(playerId):
            logging.error(f"player {playerId} is not in room {self.roomId}")
            return
        uniCards = list(set(cards))
        msg = PlayerDealInd()
        for card in cards:
            self.scoreInRound += self.cardHeap.calcCardScore(card)
            index = self.players[playerId].cards.index(card)
            if index >= 0:
                msg.cards.append(card)
                del self.players[playerId].cards[index]
        if len(self.players[playerId].cards) == 0:
            self.players[playerId].isPassing = True
        msg.playerId = playerId
        msg.roomId = self.roomId
        self.broadcast(msg)
        self.lastDealIndex = self.players[playerId].index
        if self.isGameOver():
            return
        if self.isRoundOver():
            self.startNewRound()
        else:
            self.getNextNonPassIndex()
            self.reportDealOwner()

    def handlePlayerPass(self, player):
        playerId = player.playerId
        if not self.isPlayerInRoom(playerId):
            logging.error(f"player {playerId} is not in room {self.roomId}")
            return
        msg = PlayerPassInd()
        msg.roomId = self.roomId
        msg.playerId = playerId
        self.broadcast(msg)
        self.players[playerId].isPassing = True
        if self.isRoundOver():
            self.startNewRound()
        else:
            self.reportDealOwner()

    def handlePlayerDealTimeout(self, player):
        self.handlePlayerPass(player)

    def isFull(self):
        return len(self.players) == self.maxPlayerNum

    def isEmpty(self):
        return len(self.players) == 0

    def isPlayerInRoom(self, playerId):
        return playerId in self.players

#### private
    def broadcast(self, msg):
        for id in self.players:
            self.players[id].sendMsg(msg.serialize())

    def dispatchCards(self):
        msg = DispatchCardsInd()
        msg.roomId = self.roomId
        for id in self.players:
            cardsNumNeeded = 5 - len(self.players[id].cards)
            cards = self.cardHeap.getCards(cardsNumNeeded)
            msg.cards = cards
            msg.playerId = id
            self.players[id].sendMsg(msg.serialize())
            self.players[id].cards.extend(cards)

    def generatePlayerIndex(self):
        idxs = [0 for i in range(self.maxPlayerNum)]
        for id in self.players:
            idxs[self.players[id].index] = 1
        for i in range(self.maxPlayerNum):
            if idxs[i] == 0:
                return i

    def sendRoomInfoInd(self, player):
        msg = RoomInfoInd()
        for id in self.players:
            publicInfo = PublicPlayerInfoInRoom(self.players[id].getId(), self.roomId, self.players[id].index, self.players[id].isReady)
            msg.players.append(publicInfo)
        player.sendMsg(msg.serialize())

    def sendToAllExcept(self, playerId, msg):
        for id in self.players:
            if id == playerId: continue
            self.players[id].player.sendMsg(msg.serialize())

    def areAllPlayersReady(self):
        if not self.isFull():
            return False
        for id in self.players:
            if self.players[id].isReady == False:
                return False
        return True 

    def reportDealOwner(self):
        msg = DealOwnerChangeInd()
        for id in self.players:
            if self.players[id].index == self.currentDealIndex:
                msg.playerId = id
                msg.roomId = self.roomId
                break
        self.broadcast(msg)

    def resetAllPlayerReadyStatus(self):
        for id in self.players:
            self.players[id].isReady = False

    def resetAllPlayerPassStatus(self):
        for id in self.players:
            self.players[id].isPassing = False

    def startGame(self):
        logging.info(f"The game start in room {self.roomId}")
        msg = GameStartInd()
        msg.roomId = self.roomId
        self.broadcast(msg)
        self.cardHeap.washCards()
        self.resetAllPlayerReadyStatus()
        self.startNewRound()

    def getPlayerByIndex(self, index):
        for id in self.players:
            if (self.players[id].index == index):
                return self.players[id]

    def startNewRound(self):
        if self.scoreInRound > 0:
            player = self.getPlayerByIndex(self.lastDealIndex)
            player.score += self.scoreInRound
            msg = PlayerGetScoreInd()
            msg.scoreToAdd = self.scoreInRound
            msg.scoreInTotal = player.score
            msg.roomId = self.roomId
            msg.playerId = player.getId()
            self.broadcast(msg)
            self.scoreInRound = 0
        self.currentDealIndex = self.lastDealIndex
        self.resetAllPlayerPassStatus()
        self.dispatchCards()
        self.reportDealOwner()

    def isRoundOver(self):
        nonPassingPlayerCounter = 0
        for id in self.players:
            if self.players[id].isPassing == False:
                nonPassingPlayerCounter += 1
                if nonPassingPlayerCounter > 1:
                    return False
        return True

    def isGameOver(self):
        return False

    def getNextNonPassIndex(self):
        for i in range(self.currentDealIndex+1, self.maxPlayerNum):
            for id in self.players:
                if self.players[id].isPassing == False and self.players[id].index == i:
                    self.currentDealIndex = i
                    return
        for i in range(0, self.currentDealIndex):
            for id in self.players:
                if self.players[id].isPassing == False and self.players[id].index == i:
                    self.currentDealIndex = i
                    return
        self.currentDealIndex = -1
